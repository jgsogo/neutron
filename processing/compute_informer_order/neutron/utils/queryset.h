
#pragma once

#include <vector>
#include "tuple.h"

namespace utils {

    template <typename... Args>
    using queryset = std::vector<std::tuple<Args...>>;

    template <typename T>
    std::vector<T> list(const queryset<T>& qs) {
        std::vector<T> result;
        std::transform(qs.begin(), qs.end(), std::back_inserter(result), [](auto& item) { return std::get<0>(item);});
        return result;
    }

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
}