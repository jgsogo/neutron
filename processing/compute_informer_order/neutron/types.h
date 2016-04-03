
#pragma once

#include "../utils/strong_typedef.h"

namespace neutron {
    
    typedef ::utils::strong_typedef<std::size_t, 0> informer_id;
    typedef ::utils::strong_typedef<std::size_t, 1> meaning_id;
    typedef ::utils::strong_typedef<std::size_t, 2> word_coarse_id;
    typedef ::utils::strong_typedef<std::size_t, 3> word_use_id;
    typedef ::utils::strong_typedef<std::size_t, 4> region_id;
    typedef ::utils::strong_typedef<std::size_t, 5> interface_id;
    typedef ::utils::strong_typedef<std::size_t, 6> word_id;
    
}