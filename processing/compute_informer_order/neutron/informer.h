
#pragma once

#include "queryset/models/model.h"
#include "types.h"

namespace neutron {

    class Informer : public qs::Model<informer_id, region_id, float> {
        public:
            Informer();
            Informer(const std::tuple<informer_id, region_id, float>& data);

        protected:
            informer_id _id;
            region_id _region;
            float _confidence;
    };

}
