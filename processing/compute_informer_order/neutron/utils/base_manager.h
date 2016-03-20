
#pragma once

#include "read_file.h"
#include "tuple.h"
#include "queryset.h"

namespace utils {
        
    typedef std::exception Exception;
        
    class NotFoundException : public Exception {
        public:
            NotFoundException(const char* msg) : Exception(msg) {};
    };
               
    template <typename... Args>
    class BaseManager {
        public:
            typedef queryset<Args...> queryset;
                
            static std::size_t parse(const std::string& filename, queryset& data) {
                std::size_t old_length = data.size();
                read_file<Args...>(filename, data);
                return data.size() - old_length;
            }
                
        public:
            BaseManager(const std::string& filename) {
                parse(filename, _raw_data);
            }

            template <typename T>
            auto filter(const T& filter_value) {
                return ::utils::filter(_raw_data, filter_value);
            }

            template <typename T>
            auto filter(const std::vector<T>& filter_values) {
                return ::utils::filter(_raw_data, filter_values);
            }

            const queryset& all() const {
                return _raw_data;
            }
        protected:
            queryset _raw_data;
    };     
}

