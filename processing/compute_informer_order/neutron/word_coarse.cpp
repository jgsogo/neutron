
#include "word_coarse.h"

#include <boost/filesystem.hpp>
#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

#include "manager.h"
#include "config_store.h"
#include "entropy.h"


namespace neutron {

    namespace {
        std::string word_coarse_path() {
            namespace fs = boost::filesystem;
            auto word_coarse_filename = ConfigStore::get().get_value_as<std::string>("files/wordcoarse_data");
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path(word_coarse_filename);
            return full_path.string();
        }
    }

    WordCoarseManager::WordCoarseManager() : BaseManager<WordCoarse>(word_coarse_path()) {}

    std::vector<std::pair<meaning_id, float>> WordCoarseManager::gather_entropy_data(const std::vector<Informer>& informers) {
        auto log = spdlog::get("neutron");

        auto data = this->all().filter<Informer>(informers);
        log->debug(" - data: {} samples.", data.count());

        // Compute entropy
        std::vector<std::pair<meaning_id, float>> entropy_data; // TODO: Initialize with size
        for (auto meaning: data.groupBy<meaning_id>()) {
            log->debug("   + meaning {}", meaning.first);
            // Initialize counts with at least one observation of each variable
            std::map<WordCoarseData, std::size_t> counts = {{WordCoarseData(true), 1}, {WordCoarseData(false), 1}};
            for (auto profane: meaning.second.groupBy<WordCoarseData>()) {
                log->debug("     - {}: {}", profane.first, profane.second.count());
                counts[profane.first] = profane.second.count();
            }
            auto entropy = utils::compute_entropy(counts);
            entropy_data.push_back(std::make_pair(meaning.first, entropy));
            log->debug("   => {}", entropy);
            log->info("   + meaning {}: {}", meaning.first, entropy);
        }
        return entropy_data;
    }


    std::ostream& operator << (std::ostream& os, const WordCoarseData& w) {
        return os << (w._coarse ? "profane" : "ok");
    }



    WordCoarse::WordCoarse() {
    }
    WordCoarse::WordCoarse(const BaseModel::tuple& data) : WordCoarse::BaseModel(data) {
    }

    WordCoarseManager& WordCoarse::objects() {
        static WordCoarseManager manager;
        return manager;
    }

}
