"""Export dispatcher — routes (data, format) pairs to the correct exporter."""
from __future__ import annotations

from typing import Iterable, Union

from macro_sync.schema import DailySummary, NutritionEntry

Data = Union[Iterable[NutritionEntry], Iterable[DailySummary]]

# Text formats
TEXT_FORMATS = {
    "json", "csv", "markdown", "md", "yaml", "toml", "tsv",
    "html", "xml", "ndjson", "jsonl", "latex", "geojson", "jsonlines",
}

# Binary formats
BINARY_FORMATS = {
    "xlsx", "sqlite", "parquet", "msgpack", "pdf", "ods",
    "netcdf", "arrow", "feather", "hdf5", "protobuf", "cbor",
    "avro", "orc", "pivot_xlsx", "jsonlines_gz",
}


def export(
    data: Data,
    fmt: str,
    *,
    mode: str = "entries",
) -> Union[str, bytes]:
    """Export *data* to *fmt*.

    Parameters
    ----------
    data:
        An iterable of :class:`NutritionEntry` or :class:`DailySummary`.
    fmt:
        Target format string (e.g. ``"json"``, ``"csv"``, ``"parquet"``).
    mode:
        ``"entries"`` (default) or ``"summaries"``.
    """
    items = list(data)
    fmt = fmt.lower()

    if fmt == "json":
        from macro_sync.exporters.json_exporter import entries_to_json_str, summaries_to_json_str
        return entries_to_json_str(items) if mode == "entries" else summaries_to_json_str(items)

    if fmt == "csv":
        from macro_sync.exporters.csv_exporter import entries_to_csv_str, summaries_to_csv_str
        return entries_to_csv_str(items) if mode == "entries" else summaries_to_csv_str(items)

    if fmt in ("markdown", "md"):
        from macro_sync.exporters.markdown_exporter import entries_to_markdown_str, summaries_to_markdown_str
        return entries_to_markdown_str(items) if mode == "entries" else summaries_to_markdown_str(items)

    if fmt == "yaml":
        from macro_sync.exporters.yaml_exporter import entries_to_yaml_str, summaries_to_yaml_str
        return entries_to_yaml_str(items) if mode == "entries" else summaries_to_yaml_str(items)

    if fmt == "toml":
        from macro_sync.exporters.toml_exporter import entries_to_toml_str, summaries_to_toml_str
        return entries_to_toml_str(items) if mode == "entries" else summaries_to_toml_str(items)

    if fmt == "tsv":
        from macro_sync.exporters.tsv_exporter import entries_to_tsv_str, summaries_to_tsv_str
        return entries_to_tsv_str(items) if mode == "entries" else summaries_to_tsv_str(items)

    if fmt == "html":
        from macro_sync.exporters.html_exporter import entries_to_html_str, summaries_to_html_str
        return entries_to_html_str(items) if mode == "entries" else summaries_to_html_str(items)

    if fmt == "xml":
        from macro_sync.exporters.xml_exporter import entries_to_xml_str, summaries_to_xml_str
        return entries_to_xml_str(items) if mode == "entries" else summaries_to_xml_str(items)

    if fmt == "ndjson":
        from macro_sync.exporters.ndjson_exporter import entries_to_ndjson_str, summaries_to_ndjson_str
        return entries_to_ndjson_str(items) if mode == "entries" else summaries_to_ndjson_str(items)

    if fmt == "jsonl":
        from macro_sync.exporters.jsonl_exporter import entries_to_jsonl_str, summaries_to_jsonl_str
        return entries_to_jsonl_str(items) if mode == "entries" else summaries_to_jsonl_str(items)

    if fmt == "jsonlines":
        from macro_sync.exporters.jsonlines_exporter import entries_to_jsonlines_str, summaries_to_jsonlines_str
        return entries_to_jsonlines_str(items) if mode == "entries" else summaries_to_jsonlines_str(items)

    if fmt == "latex":
        from macro_sync.exporters.latex_exporter import entries_to_latex_str, summaries_to_latex_str
        return entries_to_latex_str(items) if mode == "entries" else summaries_to_latex_str(items)

    if fmt == "geojson":
        from macro_sync.exporters.geojson_exporter import entries_to_geojson_str, summaries_to_geojson_str
        return entries_to_geojson_str(items) if mode == "entries" else summaries_to_geojson_str(items)

    if fmt == "xlsx":
        from macro_sync.exporters.excel_exporter import entries_to_excel_bytes, summaries_to_excel_bytes
        return entries_to_excel_bytes(items) if mode == "entries" else summaries_to_excel_bytes(items)

    if fmt == "sqlite":
        from macro_sync.exporters.sqlite_exporter import entries_to_sqlite_bytes, summaries_to_sqlite_bytes
        return entries_to_sqlite_bytes(items) if mode == "entries" else summaries_to_sqlite_bytes(items)

    if fmt == "parquet":
        from macro_sync.exporters.parquet_exporter import entries_to_parquet_bytes, summaries_to_parquet_bytes
        return entries_to_parquet_bytes(items) if mode == "entries" else summaries_to_parquet_bytes(items)

    if fmt == "msgpack":
        from macro_sync.exporters.msgpack_exporter import entries_to_msgpack_bytes, summaries_to_msgpack_bytes
        return entries_to_msgpack_bytes(items) if mode == "entries" else summaries_to_msgpack_bytes(items)

    if fmt == "pdf":
        from macro_sync.exporters.pdf_exporter import entries_to_pdf_bytes, summaries_to_pdf_bytes
        return entries_to_pdf_bytes(items) if mode == "entries" else summaries_to_pdf_bytes(items)

    if fmt == "ods":
        from macro_sync.exporters.ods_exporter import entries_to_ods_bytes, summaries_to_ods_bytes
        return entries_to_ods_bytes(items) if mode == "entries" else summaries_to_ods_bytes(items)

    if fmt == "netcdf":
        from macro_sync.exporters.netcdf_exporter import entries_to_netcdf_bytes, summaries_to_netcdf_bytes
        return entries_to_netcdf_bytes(items) if mode == "entries" else summaries_to_netcdf_bytes(items)

    if fmt == "arrow":
        from macro_sync.exporters.arrow_exporter import entries_to_arrow_bytes, summaries_to_arrow_bytes
        return entries_to_arrow_bytes(items) if mode == "entries" else summaries_to_arrow_bytes(items)

    if fmt == "feather":
        from macro_sync.exporters.feather_exporter import entries_to_feather_bytes, summaries_to_feather_bytes
        return entries_to_feather_bytes(items) if mode == "entries" else summaries_to_feather_bytes(items)

    if fmt == "hdf5":
        from macro_sync.exporters.hdf5_exporter import entries_to_hdf5_bytes, summaries_to_hdf5_bytes
        return entries_to_hdf5_bytes(items) if mode == "entries" else summaries_to_hdf5_bytes(items)

    if fmt == "protobuf":
        from macro_sync.exporters.protobuf_exporter import entries_to_protobuf_bytes, summaries_to_protobuf_bytes
        return entries_to_protobuf_bytes(items) if mode == "entries" else summaries_to_protobuf_bytes(items)

    if fmt == "cbor":
        from macro_sync.exporters.cbor_exporter import entries_to_cbor_bytes, summaries_to_cbor_bytes
        return entries_to_cbor_bytes(items) if mode == "entries" else summaries_to_cbor_bytes(items)

    if fmt == "avro":
        from macro_sync.exporters.avro_exporter import entries_to_avro_bytes, summaries_to_avro_bytes
        return entries_to_avro_bytes(items) if mode == "entries" else summaries_to_avro_bytes(items)

    if fmt == "orc":
        from macro_sync.exporters.orc_exporter import entries_to_orc_bytes, summaries_to_orc_bytes
        return entries_to_orc_bytes(items) if mode == "entries" else summaries_to_orc_bytes(items)

    if fmt == "pivot_xlsx":
        from macro_sync.exporters.excel_pivot_exporter import entries_to_pivot_excel_bytes
        return entries_to_pivot_excel_bytes(items)

    if fmt == "jsonlines_gz":
        from macro_sync.exporters.jsonlines_exporter import entries_to_jsonlines_bytes, summaries_to_jsonlines_bytes
        return (
            entries_to_jsonlines_bytes(items, compress=True)
            if mode == "entries"
            else summaries_to_jsonlines_bytes(items, compress=True)
        )

    raise ValueError(f"Unsupported export format: {fmt!r}")
