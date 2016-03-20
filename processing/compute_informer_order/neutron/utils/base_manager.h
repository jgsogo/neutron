
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
                
                /* TODO: Investigar cómo implementar filtros
                data_vector_type filter(const std::tuple<Args...>& filters) {
                    data_vector_type result;
                    for (auto& item: _raw_data) {
                        if(::utils::tuple::pair_compare<Args...>(item, filters)) {
                            result.push_back(item);
                        }
                    }
                    return result;
                }
                */
                
                template <typename T>
                auto filter(const std::vector<T>& filter_values) {
                    constexpr std::size_t index = ::utils::tuple::index<T, Args...>();
                    typedef ::utils::tuple::remove_ith_type<index, std::tuple<Args...>>::type result_tuple;
                    constexpr auto result_tuple_indexes = ::utils::tuple::remove_ith_type<index, std::tuple<Args...>>::indexes();

                    std::vector<result_tuple> result;

                    // There is no 'std::copy_if_and_transform' algorithm
                    for (auto& item : _raw_data) {
                        if (std::find(filter_values.begin(), filter_values.end(), std::get<index>(item)) != filter_values.end()) {
                            result.push_back(::utils::tuple::project<result_tuple_indexes>(item));
                        }
                    }
                    return result;
                }

                const data_vector_type& all() const {
                    return _raw_data;
                }
            protected:
                data_vector_type _raw_data;
        };     
    }
}
