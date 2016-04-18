
#pragma once

#include <set>
#include "queryset.h"

namespace utils {

    template <typename... Args>
    class FilterContainer {
        protected:
            class Empty : public std::runtime_error {
                public:
                    Empty() : std::runtime_error("Empty queryset") {};
            };

            class BaseFilter {
                public:
                    BaseFilter() {};
                    virtual ~BaseFilter() {};
                    virtual bool add_filter(const BaseFilter* p) = 0;
                    virtual queryset<Args...> apply(const queryset<Args...>& qs) const = 0;
            };

            template <typename T>
            class Filter : public BaseFilter {
                public:
                    Filter(const T& t) : _value(t) {};
                    ~Filter() {};

                    virtual queryset<Args...> apply(const queryset<Args...>& qs) const {
                        return filter(qs, _value);
                    };

                    virtual bool add_filter(const BaseFilter* p) {
                        const Filter<T>* ptype = dynamic_cast<const Filter<T>*>(p);
                        if (ptype) {
                            if (ptype->_value == _value) {
                                return true;
                            }
                            else {
                                throw Empty();
                            }
                        }
                        return false;
                    };

                protected:
                    T _value;
                };

            template <typename T>
            class FilterVector : public BaseFilter {
                public:
                    FilterVector(const std::vector<T>& t) : _value(t) {};
                    ~FilterVector() {};

                    virtual queryset<Args...> apply(const queryset<Args...>& qs) const {
                        return filter(qs, _value);
                    };

                    virtual bool add_filter(const BaseFilter* p) {
                        const FilterVector<T>* ptype = dynamic_cast<const FilterVector<T>*>(p);
                        if (ptype) {
                            _value.insert(ptype->_value)
                        }
                        return false;
                    };
                protected:
                    std::set<T> _value;
            };

        public:
            FilterContainer() : _is_empty(false) {};
            ~FilterContainer() {
                for (auto& filter : _filters) {
                    delete filter;
                }
                _filters.clear();
            };

            queryset<Args...> apply(const queryset<Args...>& qs) const {
                if (_is_empty) {
                    return queryset<Args...>();
                }
                queryset<Args...> result(qs);
                for (auto& filter : _filters) {
                    result = filter->apply(result);
                }
                return result;
            };

            template <typename T>
            void add_filter(const T& t) {
                Filter<T>* new_filter = new Filter<T>(t);
                bool considered = false;
                try {
                    for (auto& filter : _filters) {
                        considered |= filter->add_filter(new_filter);
                    }
                    if (!considered) {
                        _filters.push_back(new_filter);
                    }
                    else {
                        delete new_filter;
                    }
                }
                catch (Empty&) {
                    _is_empty = true;
                }
            };

            template <typename T>
            void add_filter(const std::vector<T>& t) {
                FilterVector<T>* new_filter = new FilterVector<T>(t);
                bool considered = false;
                try {
                    for (auto& filter : _filters) {
                        considered |= filter->add_filter(new_filter);
                    }
                    if (!considered) {
                        _filters.push_back(new_filter);
                    }
                    else {
                        delete new_filter;
                    }
                }
                catch (Empty& e) {
                    _is_empty = true;
                }
            };

            template <typename... T>
            void add_filter(const std::tuple<T...>& t) {
                this->add_filter(std::get<0>(t));
                this->add_filter(::utils::tuple::tail(t));
            };

            template <typename T>
            void add_filter(const std::tuple<T>& t) {
                this->add_filter(std::get<0>(t));
            };

        protected:
            bool _is_empty;
            std::vector<BaseFilter*> _filters;
    };
    
}
