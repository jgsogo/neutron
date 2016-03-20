
#pragma once

#include <tuple>
#include <utility>

namespace utils {
    namespace tuple {
        
        // Credit: http://stackoverflow.com/questions/10626856/how-to-split-a-tuple
        
        template < typename T , typename... Ts >
        auto head( std::tuple<T,Ts...> t )
        {
           return  std::get<0>(t);
        }

        template < std::size_t... Ns , typename... Ts >
        auto tail_impl( std::index_sequence<Ns...> , std::tuple<Ts...> t )
        {
           return  std::make_tuple( std::get<Ns+1u>(t)... );
        }

        template < typename... Ts >
        auto tail( std::tuple<Ts...> t )
        {
           return  tail_impl( std::make_index_sequence<sizeof...(Ts) - 1u>() , t );
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

