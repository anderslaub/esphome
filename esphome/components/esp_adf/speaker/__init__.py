import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import speaker
from esphome.const import CONF_ID

from .. import (
    CONF_ESP_ADF_ID,
    ESPADF,
    ESPADFPipeline,
    esp_adf_ns,
    final_validate_usable_board,
)

CONF_SPEAKER_VOLUME = "volume"

AUTO_LOAD = ["esp_adf"]
CONFLICTS_WITH = ["i2s_audio"]
DEPENDENCIES = ["esp32"]

ESPADFSpeaker = esp_adf_ns.class_(
    "ESPADFSpeaker", ESPADFPipeline, speaker.Speaker, cg.Component
)


CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(ESPADFSpeaker),
            cv.GenerateID(CONF_ESP_ADF_ID): cv.use_id(ESPADF),
            cv.Optional(CONF_SPEAKER_VOLUME, default=50): cv.int_range(min=0, max=100),
        }
    ).extend(cv.COMPONENT_SCHEMA),
    cv.only_with_esp_idf,
)

SETTERS = {
    # pin assignment
    CONF_SPEAKER_VOLUME: "set_volume"
}

FINAL_VALIDATE_SCHEMA = final_validate_usable_board("speaker")


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await cg.register_parented(var, config[CONF_ESP_ADF_ID])
    await speaker.register_speaker(var, config)
    cg.add(var.set_volume(config[CONF_SPEAKER_VOLUME]))
