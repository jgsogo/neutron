
#pragma once

#include "queryset.h"

namespace utils {

    class BaseFilter {
        public:
            BaseFilter() {};
            virtual ~BaseFilter() = 0;
    };

    class FilterContainer {
        public:
            FilterContainer() {};
            ~FilterContainer() {};

            template <typename... Args>
            queryset<Args...> apply(const queryset<Args...>& qs) const {
                return qs;
            };
        protected:
            std::vector<BaseFilter*> _filters;
    };

    class EmptyQuerySetFilter {
        public:
            EmptyQuerySetFilter() {};
            ~EmptyQuerySetFilter() {};
            
            template <typename... Args>
            queryset<Args...> apply(const queryset<Args...>& qs) {
                return queryset<Args...>(); // returns empty queryset
            };
    };

    template <typename T>
    class Filter : public BaseFilter {
        public:
            Filter(const T& t) : _value(t) {};

            template <typename... Args>
            queryset<Args...> apply(const queryset<Args...>& qs) {
                return filter(qs, _value);
            };

        protected:
            T _value;
    };

    template <typename T>
    class FilterVector : public BaseFilter {
        public:
            FilterVector(const std::vector<T>& t) : _value(t) {};
    
            template <typename... Args>
            queryset<Args...> apply(const queryset<Args...>& qs) {
                return filter(qs, _value);
            };
    protected:
            std::vector<T> _value;
    };

    template <typename... T>
    class MultiFilter : public BaseFilter {
        public:
            MultiFilter(const std::tuple<T...>& t) : _value(t) {};
            
            template <typename... Args>
            queryset<Args...> apply(const queryset<Args...>& qs) {
                return filter(qs, _value);
            };
        protected:
            std::tuple<T...> _value;
    };


}
