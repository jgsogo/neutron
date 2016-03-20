
#pragma once

#include <tuple>
#include <utility>

namespace utils {
    namespace tuple {
        
        // References: 
        //  - tail/head: http://stackoverflow.com/questions/10626856/how-to-split-a-tuple
        //  - project: http://stackoverflow.com/questions/23612648/creating-a-c-stdtuple-projection-function
        
        // Projection
        namespace {
            template<typename T, size_t... indexes>
            class Projection {
                public:
                    using Tuple = std::tuple<typename std::tuple_element<indexes, T>::type...>;
            };

            template < std::size_t... Ns, typename... Ts >
            auto tail_impl(std::index_sequence<Ns...>, std::tuple<Ts...> t) {
                return std::make_tuple(std::get<Ns + 1u>(t)...);
            }
        }

        template < typename T , typename... Ts >
        auto head( std::tuple<T,Ts...> t ) {
           return  std::get<0>(t);
        }

        template < typename... Ts >
        auto tail( std::tuple<Ts...> t ) {
           return  tail_impl( std::make_index_sequence<sizeof...(Ts) - 1u>() , t );
        }

        template<size_t... indexes, typename T>
        auto project(const T &t) -> typename Projection<T, indexes...>::Tuple {
            return typename Projection<T, indexes...>::Tuple(std::get<indexes>(t)...);
        }

        // Comparaison
        struct NoCompareType {};
        namespace {
            template <typename T, typename U = T>
            struct atomic_compare {
                static bool pair_compare(const T& lhs, const U& rhs) {
                    return (lhs == rhs);
                }
            };
            
            template <typename T>
            struct atomic_compare<T, NoCompareType> {
                static bool pair_compare(const T& lhs, const NoCompareType& rhs) {return true;}
            };
            
            template <typename T>
            struct atomic_compare<NoCompareType, T> {
                static bool pair_compare(const NoCompareType& lhs, const T& rhs) {return true;}
            };
                        
        }
        
        
        template <typename T, typename... Args>
        bool pair_compare(const std::tuple<T, Args...>& lhs, const std::tuple<T, Args...>& rhs) {
            return atomic_compare<T>::pair_compare(head(lhs), head(rhs)) && 
                   pair_compare<Args...>(tail(lhs), tail(rhs));
        }
        
        template <typename T>
        bool pair_compare(const std::tuple<T>& lhs, const std::tuple<T>& rhs) {
            return atomic_compare<T>::pair_compare(head(lhs), head(rhs));
        }
        
    }
}

