from dl_connector_bundle_chs3.file.formula.utils import clickhouse_funcs_for_file_dialect
from dl_connector_clickhouse.formula.definitions.functions_special import DEFINITIONS_SPECIAL as CH_DEFINITIONS_SPECIAL


DEFINITIONS_SPECIAL = clickhouse_funcs_for_file_dialect(CH_DEFINITIONS_SPECIAL)
