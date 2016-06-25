
#pragma once

#include "queryset/models/manager.h"

namespace neutron {

    template <typename TModel>
    class BaseManager : public qs::FileManager<TModel> {
        public:
            BaseManager(const std::string& filename) : qs::FileManager<TModel>(filename) {}

    };

}
