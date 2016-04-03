
#pragma once

#include <vector>
#include "tuple.h"

namespace utils {

    // A queryset is just a vector of tuples of a given type
    template <typename... Args>
    using queryset = std::vector<std::tuple<Args...>>;

    // We can list a queryset for one of its values (it is like projecting and then flattening to a vector)
    template <typename T, typename... Args>
    typename std::vector<T> list(const queryset<Args...>& qs) {
        std::vector<T> result;
        std::transform(qs.begin(), qs.end(), std::back_inserter(result), [](auto& item) { 
            constexpr std::size_t index = ::utils::tuple::index<T, Args...>();
            return std::get<index>(item);
            });
        return result;
    }

    // Filter a queryset by one value in a column
    template <typename... Args, typename T>
    auto filter(const queryset<Args...>& qs, const T& filter_value) {
        constexpr std::size_t index = ::utils::tuple::index<T, Args...>();
        typedef ::utils::tuple::remove_ith_type<index, std::tuple<Args...>>::type result_tuple;
        typedef ::utils::tuple::gen_seq<sizeof...(Args), index>::type result_tuple_indexes;

        std::vector<result_tuple> result;
        // There is no 'std::copy_if_and_transform' algorithm
        for (auto& item : qs) {
            if (std::get<index>(item) == filter_value) {
                result.push_back(::utils::tuple::project(item, result_tuple_indexes()));
            }
        }
        return result;
    }

    // Filter a queryset by several values in a given column
    template <typename... Args, typename T>
    auto filter(const queryset<Args...>& qs, const std::vector<T>& filter_values) {
        constexpr std::size_t index = ::utils::tuple::index<T, Args...>();
        typedef ::utils::tuple::remove_ith_type<index, std::tuple<Args...>>::type result_tuple;
        typedef ::utils::tuple::gen_seq<sizeof...(Args), index>::type result_tuple_indexes;

        std::vector<result_tuple> result;
        // There is no 'std::copy_if_and_transform' algorithm
        for (auto& item : qs) {
            if (std::find(filter_values.begin(), filter_values.end(), std::get<index>(item)) != filter_values.end()) {
                result.push_back(::utils::tuple::project(item, result_tuple_indexes()));
            }
        }
        return result;
    }

    // Project a queryset over a set of column (delete the rest of columns)
    template <typename T, typename... Args>
    auto project(const queryset<Args...>& qs) {
        constexpr std::size_t index = ::utils::tuple::index<T, Args...>();
        typedef ::utils::tuple::remove_ith_type<index, std::tuple<Args...>>::type result_tuple;
        typedef ::utils::tuple::gen_seq<sizeof...(Args), index>::type result_tuple_indexes;

        std::vector<result_tuple> result;
        for (auto& item : qs) {
            result.push_back(::utils::tuple::project(item, result_tuple_indexes()));
        }
        return result;
    }


    template <typename... Args>
    class QuerySet {
        public:
            QuerySet(const queryset<Args...>& qs) : _qs(qs) {};  // TODO: Move input qs to QuerySet ¿?
            /*
            template <typename T>
            auto filter(const T& filter_value) {
                return QuerySet<Args...>(::utils::filter(_qs, filter_value));
            };
            */
        protected:
            queryset<Args...> _qs;
    };

}
