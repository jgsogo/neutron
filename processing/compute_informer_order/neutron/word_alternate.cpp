
#include "word_alternate.h"

#include <boost/filesystem.hpp>
#include <spdlog/spdlog.h>
#include <spdlog/fmt/ostr.h>

#include "manager.h"
#include "config_store.h"
#include "entropy.h"


namespace neutron {

    namespace {
        std::string word_alternate_path() {
            namespace fs = boost::filesystem;
            auto word_alternate_filename = ConfigStore::get().get_value_as<std::string>("files/wordalternate_data");
            fs::path full_path = ConfigStore::get().get_value_as<std::string>("db_path") / fs::path(word_alternate_filename);
            return full_path.string();
        }
    }

    WordAlternateManager::WordAlternateManager() : BaseManager<WordAlternate>(word_alternate_path()) {}

    std::vector<std::pair<meaning_id, float>> WordAlternateManager::gather_entropy_data(const std::vector<Informer>& informers) {
        auto log = spdlog::get("neutron");

        auto data = this->all().filter<Informer>(informers);
        log->debug(" - data: {} samples.", data.count());

        // Compute entropy
        std::vector<std::pair<meaning_id, float>> entropy_data; // TODO: Initialize with size
        for (auto meaning: data.groupBy<meaning_id>()) {
            log->debug("   + meaning {}", meaning.first);
            // Initialize counts with at least one observation of each variable
            std::map<word_id, std::size_t> counts;
            for (auto alternate: meaning.second.groupBy<word_id>()) {
                log->debug("     - {}: {}", alternate.first, alternate.second.count());
                counts[alternate.first] = alternate.second.count();
            }
            auto entropy = utils::compute_entropy(counts);
            entropy_data.push_back(std::make_pair(meaning.first, entropy));
            log->debug("   => {}", entropy);
            log->info("   + meaning {}: {}", meaning.first, entropy);
        }

        return entropy_data;
    }


    WordAlternate::WordAlternate() {
    }
    WordAlternate::WordAlternate(const BaseModel::tuple& data) : WordAlternate::BaseModel(data) {
    }

    WordAlternateManager& WordAlternate::objects() {
        static WordAlternateManager manager;
        return manager;
    }

}
