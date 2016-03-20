
#pragma once

#include "read_file.h"
#include "tuple.h"

namespace neutron {
    namespace utils {
        
        typedef std::exception Exception;
        
        class NotFoundException : public Exception {
            public:
                NotFoundException(const char* msg) : Exception(msg) {};
        };
               
        template <typename... Args>
        class BaseManager {
            public:
                typedef std::vector<std::tuple<Args...>> data_vector_type;
                
                static std::size_t parse(const std::string& filename, data_vector_type& data) {
                    std::size_t old_length = data.size();
                    utils::read_file<Args...>(filename, data);
                    return data.size() - old_length;
                }
                
            public:
                BaseManager(const std::string& filename) {
                    parse(filename, _raw_data);
                }
                
                data_vector_type filter(const std::tuple<Args...>& filters) {
                    data_vector_type result;
                    for (auto& item: _raw_data) {
                        if(::utils::tuple::pair_compare<Args...>(item, filters)) {
                            result.push_back(item);
                        }
                    }
                    return result;
                }
                
            protected:
                data_vector_type _raw_data;
        };     
    }
}