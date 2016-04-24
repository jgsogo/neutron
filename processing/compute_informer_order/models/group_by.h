
#pragma once

#include <map>
#include "queryset.h"


namespace utils {

    class GroupBy {
        public:
            template <typename T, typename... Args>
            static std::map<T, queryset<Args...>> apply(const queryset<Args...>& qs, const utils::FilterContainer<Args...>& filters) {
                typename std::map<T, queryset<Args...>> result;
                constexpr std::size_t index = tuple::index<T, Args...>();
                for (auto& item: qs) {
                    if (filters.pass(item)) {
                        result[std::get<index>(item)].push_back(item);
                    }
                }
                return result;
            }

            template <typename... T, typename... Args, typename = typename std::enable_if<(sizeof...(T) >1), bool>::type>
            static std::map<std::tuple<T...>, queryset<Args...>> apply(const queryset<Args...>& qs, const utils::FilterContainer<Args...>& filters) {
                typename std::map<std::tuple<T...>, queryset<Args...>> result;
                for (auto& item: qs) {
                    if (filters.pass(item)) {
                        typename std::tuple<T...> tup = std::make_tuple(std::get<::utils::tuple::index<T, Args...>()>(item)...);
                        result[tup].push_back(item);
                        }
                }
                return result;
            }

    };

}