
#pragma once

#include <map>
#include "queryset/base_manager.h"
#include "types.h"

namespace neutron {
    class InformerManager : public ::utils::BaseManager<informer_id, region_id, float> {
        public:
            InformerManager(const std::string& filename);
            int get_by_region(const region_id& region);

    };
}
