
#pragma once

#include "queryset/models/model.h"
#include "types.h"
#include "manager.h"

namespace neutron {

    class RegionManager : public BaseManager<region_id, region_id, std::string> {
    public:
        RegionManager();
    };

    class Region : public qs::BaseModel<RegionManager> {
        using BaseModel = qs::BaseModel<RegionManager>;
        public:
            Region();
            Region(const Region& other);
            Region(const RegionManager::tuple& data);
            virtual ~Region() {};

        protected:
            
    };
}
/*
template<class Ch, class Tr>
std::basic_ostream<Ch, Tr>& operator<<(std::basic_ostream<Ch, Tr>& os, const neutron::Region& rhs) {
    rhs.serialize(os);
    return os;
}
*/
