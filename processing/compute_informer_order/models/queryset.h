
#pragma once

#include "utils/queryset.h"
#include "filters.h"


template <typename... Args>
class QuerySet {
    public:
        QuerySet(const utils::queryset<Args...>& qs) : _qs(qs) {};  // TODO: Move input qs to QuerySet ¿?

        bool empty() const {
            return _filters.empty();
        }

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

        utils::queryset<Args...> get() const {
            return _filters.apply(_qs);
        }

    protected:
        utils::queryset<Args...> _qs;
        utils::FilterContainer<Args...> _filters;
};
