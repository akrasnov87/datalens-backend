from dl_connector_bundle_chs3.file.formula.utils import clickhouse_funcs_for_file_dialect
from dl_connector_clickhouse.formula.definitions.operators_ternary import DEFINITIONS_TERNARY as CH_DEFINITIONS_TERNARY


DEFINITIONS_TERNARY = clickhouse_funcs_for_file_dialect(CH_DEFINITIONS_TERNARY)