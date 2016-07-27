
#pragma once

#include <numeric>

namespace utils {

    float compute_information(const float& value) {
        assert(value >= 0.f && value <= 1.f); // It must be a  probability
        return (value == 0.f) ? 0.f : -value*std::log2(value);
    }

    template <typename T>
    float compute_entropy(const typename std::map<T, std::size_t>& data) {
        using value_type = typename std::pair<T, std::size_t>;
        float total_count = std::accumulate(data.begin(), data.end(), 0.f,
                                            [](const float& t, const value_type& v) {
                                                  return t + v.second;
                                            });
        if (total_count != 0.f) {
            return std::accumulate(data.begin(), data.end(), 0.f,
                                   [total_count](const float& t, const value_type& v) {
                                        return t + compute_information(v.second/total_count);
                                   });
            }
        else {
            return 0.f;
        }
    }
}
