
#pragma once

#include <map>
#include "queryset/queryset.h"
#include "types.h"

namespace neutron {

    class RegionManager {
        public:
            RegionManager(const std::string& filename);

            std::size_t count() const;
        protected:
            utils::queryset<region_id, region_id, std::string> _data;
    };
}
