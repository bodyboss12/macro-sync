"""Export dispatcher — routes to the correct exporter based on format string."""
from __future__ import annotations

from typing import List, Union

from macro_sync.schema import DailySummary, NutritionEntry

Text = str
Binary = bytes
Result = Union[Text, Binary]

_TEXT_FORMATS = {
    "json", "csv", "markdown", "md", "yaml", "toml", "tsv",
    "html", "xml", "latex", "ndjson", "jsonl",
}

_BINARY_FORMATS = {
    "excel", "xlsx", "sqlite", "parquet", "arrow", "feather",
    "msgpack", "pdf", "ods", "netcdf", "hdf5", "protobuf",
    "cbor", "avro", "orc",
}


def export(
    data: Union[List[NutritionEntry], List[DailySummary]],
    fmt: str,
    mode: str = "entries",
) -> Result:
    """Export *data* to the given format.

    Parameters
    ----------
    data:
        A list of NutritionEntry or DailySummary objects.
    fmt:
        Target format identifier (e.g. ``"json"``, ``"csv"``, ``"parquet"``).
    mode:
        ``"entries"`` or ``"summaries"``.
    """
    fmt = fmt.lower().strip()

    if fmt in ("json",):
        from macro_sync.exporters.json_exporter import entries_to_json_str, summaries_to_json_str
        fn = entries_to_json_str if mode == "entries" else summaries_to_json_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("csv",):
        from macro_sync.exporters.csv_exporter import entries_to_csv_str, summaries_to_csv_str
        fn = entries_to_csv_str if mode == "entries" else summaries_to_csv_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("markdown", "md"):
        from macro_sync.exporters.markdown_exporter import entries_to_markdown_str, summaries_to_markdown_str
        fn = entries_to_markdown_str if mode == "entries" else summaries_to_markdown_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("excel", "xlsx"):
        from macro_sync.exporters.excel_exporter import entries_to_excel_bytes, summaries_to_excel_bytes
        fn = entries_to_excel_bytes if mode == "entries" else summaries_to_excel_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("sqlite",):
        from macro_sync.exporters.sqlite_exporter import entries_to_sqlite_bytes, summaries_to_sqlite_bytes
        fn = entries_to_sqlite_bytes if mode == "entries" else summaries_to_sqlite_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("parquet",):
        from macro_sync.exporters.parquet_exporter import entries_to_parquet_bytes, summaries_to_parquet_bytes
        fn = entries_to_parquet_bytes if mode == "entries" else summaries_to_parquet_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("yaml",):
        from macro_sync.exporters.yaml_exporter import entries_to_yaml_str, summaries_to_yaml_str
        fn = entries_to_yaml_str if mode == "entries" else summaries_to_yaml_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("toml",):
        from macro_sync.exporters.toml_exporter import entries_to_toml_str, summaries_to_toml_str
        fn = entries_to_toml_str if mode == "entries" else summaries_to_toml_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("tsv",):
        from macro_sync.exporters.tsv_exporter import entries_to_tsv_str, summaries_to_tsv_str
        fn = entries_to_tsv_str if mode == "entries" else summaries_to_tsv_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("html",):
        from macro_sync.exporters.html_exporter import entries_to_html_str, summaries_to_html_str
        fn = entries_to_html_str if mode == "entries" else summaries_to_html_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("xml",):
        from macro_sync.exporters.xml_exporter import entries_to_xml_str, summaries_to_xml_str
        fn = entries_to_xml_str if mode == "entries" else summaries_to_xml_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("latex",):
        from macro_sync.exporters.latex_exporter import entries_to_latex_str, summaries_to_latex_str
        fn = entries_to_latex_str if mode == "entries" else summaries_to_latex_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("msgpack",):
        from macro_sync.exporters.msgpack_exporter import entries_to_msgpack_bytes, summaries_to_msgpack_bytes
        fn = entries_to_msgpack_bytes if mode == "entries" else summaries_to_msgpack_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("pdf",):
        from macro_sync.exporters.pdf_exporter import entries_to_pdf_bytes, summaries_to_pdf_bytes
        fn = entries_to_pdf_bytes if mode == "entries" else summaries_to_pdf_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("ndjson",):
        from macro_sync.exporters.ndjson_exporter import entries_to_ndjson_str, summaries_to_ndjson_str
        fn = entries_to_ndjson_str if mode == "entries" else summaries_to_ndjson_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("ods",):
        from macro_sync.exporters.ods_exporter import entries_to_ods_bytes, summaries_to_ods_bytes
        fn = entries_to_ods_bytes if mode == "entries" else summaries_to_ods_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("jsonl",):
        from macro_sync.exporters.jsonl_exporter import entries_to_jsonl_str, summaries_to_jsonl_str
        fn = entries_to_jsonl_str if mode == "entries" else summaries_to_jsonl_str
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("netcdf",):
        from macro_sync.exporters.netcdf_exporter import entries_to_netcdf_bytes, summaries_to_netcdf_bytes
        fn = entries_to_netcdf_bytes if mode == "entries" else summaries_to_netcdf_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("arrow",):
        from macro_sync.exporters.arrow_exporter import entries_to_arrow_bytes, summaries_to_arrow_bytes
        fn = entries_to_arrow_bytes if mode == "entries" else summaries_to_arrow_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("feather",):
        from macro_sync.exporters.feather_exporter import entries_to_feather_bytes, summaries_to_feather_bytes
        fn = entries_to_feather_bytes if mode == "entries" else summaries_to_feather_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("hdf5",):
        from macro_sync.exporters.hdf5_exporter import entries_to_hdf5_bytes, summaries_to_hdf5_bytes
        fn = entries_to_hdf5_bytes if mode == "entries" else summaries_to_hdf5_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("protobuf",):
        from macro_sync.exporters.protobuf_exporter import entries_to_protobuf_bytes, summaries_to_protobuf_bytes
        fn = entries_to_protobuf_bytes if mode == "entries" else summaries_to_protobuf_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("cbor",):
        from macro_sync.exporters.cbor_exporter import entries_to_cbor_bytes, summaries_to_cbor_bytes
        fn = entries_to_cbor_bytes if mode == "entries" else summaries_to_cbor_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("avro",):
        from macro_sync.exporters.avro_exporter import entries_to_avro_bytes, summaries_to_avro_bytes
        fn = entries_to_avro_bytes if mode == "entries" else summaries_to_avro_bytes
        return fn(data)  # type: ignore[arg-type]

    if fmt in ("orc",):
        from macro_sync.exporters.orc_exporter import entries_to_orc_bytes, summaries_to_orc_bytes
        fn = entries_to_orc_bytes if mode == "entries" else summaries_to_orc_bytes
        return fn(data)  # type: ignore[arg-type]

    raise ValueError(f"Unsupported export format: {fmt!r}")
