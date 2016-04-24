
#pragma once

#include "utils/queryset.h"
#include "filters.h"
#include "group_by.h"


template <typename... Args>
class QuerySet {
    public:
        QuerySet(const utils::queryset<Args...>& qs) : _qs(qs) {};  // TODO: Move input qs to QuerySet �?

        bool empty() const {
            return _filters.empty();
        }

        utils::queryset<Args...> get() const {
            return _filters.apply(_qs);
        }

        // Filtering functions
        template <typename T>
        QuerySet<Args...>& filter(const T& filter_value) {
            _filters.add_filter(filter_value);
            return *this;
        }

        template <typename T>
        QuerySet<Args...>& filter(const std::vector<T>& filter_value) {
            _filters.add_filter(filter_value);
            return *this;
        }

        template <typename... T>
        QuerySet<Args...>& filter(const std::tuple<T...>& filter_value) {
            _filters.add_filter(filter_value);
            return *this;
        }

        // Grouping by field types
        template <typename T>
        std::map<T, utils::queryset<Args...>> groupBy() {
            // Put all with the same value of T into a group
            return utils::GroupBy::apply<T>(_qs, _filters);
        }

        /* TODO: Work in progress.
         * Para implementar este tipo de 'group_by' podría considerar implementar utils::typle::project<T...>
         * y ya lo tendría hecho.
        template <typename... T, typename = typename std::enable_if<(sizeof...(T) > 1), bool>::type>
        std::map<std::tuple<T...>, utils::queryset<Args...>> groupBy() {
            // Put all with the same values of T... into a group
            return utils::GroupBy::apply<T...>(_qs);
        }
        */

    protected:
        utils::queryset<Args...> _qs;
        utils::FilterContainer<Args...> _filters;
        //utils::GroupBy<Args...> _groups;
};
