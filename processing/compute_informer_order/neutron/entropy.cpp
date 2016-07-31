
#include "entropy.h"

#include <cmath>
#include <assert.h>

namespace utils {

    float compute_information(const float& value) {
        assert(value >= 0.f && value <= 1.f); // It must be a  probability
        return (value == 0.f) ? 0.f : -value*std::log2(value);
    }

}
