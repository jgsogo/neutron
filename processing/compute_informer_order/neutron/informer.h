
#pragma once

#include "queryset/models/model.h"
#include "types.h"
#include "manager.h"

namespace neutron {

    class InformerManager : public BaseManager<informer_id, region_id, float> {
        public:
            InformerManager();
    };

    class Informer : public qs::BaseModel<InformerManager, informer_id, region_id, float> {
        using BaseModel = qs::BaseModel<InformerManager, informer_id, region_id, float>;
        public:
            Informer();
            Informer(const std::tuple<informer_id, region_id, float>& data);

    };

}
