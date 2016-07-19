
#pragma once

#include <numeric>

namespace utils {

    float compute_information(const std::size_t& value) {
        return (value == 0) ? 0 : -value*std::log2(value);
    }

    template <typename T>
    float compute_entropy(const typename std::map<T, std::size_t>& data) {
        using value_type = typename std::pair<T, std::size_t>;
        std::size_t total_count = std::accumulate(data.begin(), data.end(), 0.f,
                                                  [](const float& t, const value_type& v) {
                                                        return t + v.second;
                                                  });
    }

}
