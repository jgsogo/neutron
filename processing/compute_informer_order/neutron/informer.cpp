
#include "informer.h"

namespace neutron {
    Informer::Informer() {
    }

    Informer::Informer(const std::tuple<informer_id, region_id, float>& data) {
        _id = std::get<0>(data);
        _region = std::get<1>(data);
        _confidence = std::get<2>(data);
    }
}
