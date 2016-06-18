
#pragma once

#include "queryset/models/model.h"
#include "types.h"
#include "manager.h"

namespace neutron {

    class RegionManager : public BaseManager<region_id, region_id, std::string> {
    public:
        RegionManager();
    };

    class Region : public qs::BaseModel<RegionManager, region_id, region_id, std::string> {
        using BaseModel = qs::BaseModel<RegionManager, region_id, region_id, std::string>;
        public:
            Region();
            Region(const std::tuple<region_id, region_id, std::string>& data);
    };
}
