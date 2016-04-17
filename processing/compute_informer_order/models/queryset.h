
#pragma once

#include "utils/queryset.h"
#include "filters.h"


template <typename... Args>
class QuerySet {
    public:
        QuerySet(const utils::queryset<Args...>& qs) : _qs(qs) {};  // TODO: Move input qs to QuerySet ¿?

        template <typename T>
        auto filter(const T& filter_value) {
            return *this;
        }

        /*
        template <typename T>
        auto filter(const T& filter_value) {
            return QuerySet<Args...>(::utils::filter(_qs, filter_value));
        };
        */

        utils::queryset<Args...> get() const {
            return _filters.apply(_qs);
        };

    protected:
        utils::queryset<Args...> _qs;
        utils::FilterContainer _filters;
};
