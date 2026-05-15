"""Export dispatcher — routes to the correct exporter based on format string."""
from __future__ import annotations

from typing import List, Union

from macro_sync.schema import DailySummary, NutritionEntry

Text = str
Binary = bytes


def export(
    fmt: str,
    entries: List[NutritionEntry] | None = None,
    summaries: List[DailySummary] | None = None,
) -> Union[Text, Binary]:
    """Dispatch serialization to the appropriate exporter module.

    Parameters
    ----------
    fmt:
        Output format identifier (e.g. ``"json"``, ``"csv"``, ``"avro"`` …).
    entries:
        List of :class:`NutritionEntry` objects to export (mutually exclusive
        with *summaries* for most formats).
    summaries:
        List of :class:`DailySummary` objects to export.

    Returns
    -------
    str or bytes depending on the format.
    """
    if entries is None and summaries is None:
        raise ValueError("Provide either entries or summaries.")

    use_summaries = summaries is not None and entries is None

    fmt = fmt.lower()

    if fmt == "json":
        from macro_sync.exporters.json_exporter import entries_to_json_str, summaries_to_json_str
        return summaries_to_json_str(summaries) if use_summaries else entries_to_json_str(entries)

    if fmt == "csv":
        from macro_sync.exporters.csv_exporter import entries_to_csv_str, summaries_to_csv_str
        return summaries_to_csv_str(summaries) if use_summaries else entries_to_csv_str(entries)

    if fmt == "tsv":
        from macro_sync.exporters.tsv_exporter import entries_to_tsv_str, summaries_to_tsv_str
        return summaries_to_tsv_str(summaries) if use_summaries else entries_to_tsv_str(entries)

    if fmt == "markdown":
        from macro_sync.exporters.markdown_exporter import entries_to_markdown_str, summaries_to_markdown_str
        return summaries_to_markdown_str(summaries) if use_summaries else entries_to_markdown_str(entries)

    if fmt == "html":
        from macro_sync.exporters.html_exporter import entries_to_html_str, summaries_to_html_str
        return summaries_to_html_str(summaries) if use_summaries else entries_to_html_str(entries)

    if fmt == "xml":
        from macro_sync.exporters.xml_exporter import entries_to_xml_str, summaries_to_xml_str
        return summaries_to_xml_str(summaries) if use_summaries else entries_to_xml_str(entries)

    if fmt == "yaml":
        from macro_sync.exporters.yaml_exporter import entries_to_yaml_str, summaries_to_yaml_str
        return summaries_to_yaml_str(summaries) if use_summaries else entries_to_yaml_str(entries)

    if fmt == "toml":
        from macro_sync.exporters.toml_exporter import entries_to_toml_str, summaries_to_toml_str
        return summaries_to_toml_str(summaries) if use_summaries else entries_to_toml_str(entries)

    if fmt == "latex":
        from macro_sync.exporters.latex_exporter import entries_to_latex_str, summaries_to_latex_str
        return summaries_to_latex_str(summaries) if use_summaries else entries_to_latex_str(entries)

    if fmt == "ndjson":
        from macro_sync.exporters.ndjson_exporter import entries_to_ndjson_str, summaries_to_ndjson_str
        return summaries_to_ndjson_str(summaries) if use_summaries else entries_to_ndjson_str(entries)

    if fmt == "jsonl":
        from macro_sync.exporters.jsonl_exporter import entries_to_jsonl_str, summaries_to_jsonl_str
        return summaries_to_jsonl_str(summaries) if use_summaries else entries_to_jsonl_str(entries)

    # --- binary formats ---
    if fmt == "excel":
        from macro_sync.exporters.excel_exporter import entries_to_excel_bytes, summaries_to_excel_bytes
        return summaries_to_excel_bytes(summaries) if use_summaries else entries_to_excel_bytes(entries)

    if fmt == "sqlite":
        from macro_sync.exporters.sqlite_exporter import entries_to_sqlite_bytes, summaries_to_sqlite_bytes
        return summaries_to_sqlite_bytes(summaries) if use_summaries else entries_to_sqlite_bytes(entries)

    if fmt == "parquet":
        from macro_sync.exporters.parquet_exporter import entries_to_parquet_bytes, summaries_to_parquet_bytes
        return summaries_to_parquet_bytes(summaries) if use_summaries else entries_to_parquet_bytes(entries)

    if fmt == "arrow":
        from macro_sync.exporters.arrow_exporter import entries_to_arrow_bytes, summaries_to_arrow_bytes
        return summaries_to_arrow_bytes(summaries) if use_summaries else entries_to_arrow_bytes(entries)

    if fmt == "feather":
        from macro_sync.exporters.feather_exporter import entries_to_feather_bytes, summaries_to_feather_bytes
        return summaries_to_feather_bytes(summaries) if use_summaries else entries_to_feather_bytes(entries)

    if fmt == "msgpack":
        from macro_sync.exporters.msgpack_exporter import entries_to_msgpack_bytes, summaries_to_msgpack_bytes
        return summaries_to_msgpack_bytes(summaries) if use_summaries else entries_to_msgpack_bytes(entries)

    if fmt == "cbor":
        from macro_sync.exporters.cbor_exporter import entries_to_cbor_bytes, summaries_to_cbor_bytes
        return summaries_to_cbor_bytes(summaries) if use_summaries else entries_to_cbor_bytes(entries)

    if fmt == "protobuf":
        from macro_sync.exporters.protobuf_exporter import entries_to_protobuf_bytes, summaries_to_protobuf_bytes
        return summaries_to_protobuf_bytes(summaries) if use_summaries else entries_to_protobuf_bytes(entries)

    if fmt == "pdf":
        from macro_sync.exporters.pdf_exporter import entries_to_pdf_bytes, summaries_to_pdf_bytes
        return summaries_to_pdf_bytes(summaries) if use_summaries else entries_to_pdf_bytes(entries)

    if fmt == "ods":
        from macro_sync.exporters.ods_exporter import entries_to_ods_bytes, summaries_to_ods_bytes
        return summaries_to_ods_bytes(summaries) if use_summaries else entries_to_ods_bytes(entries)

    if fmt == "hdf5":
        from macro_sync.exporters.hdf5_exporter import entries_to_hdf5_bytes, summaries_to_hdf5_bytes
        return summaries_to_hdf5_bytes(summaries) if use_summaries else entries_to_hdf5_bytes(entries)

    if fmt == "netcdf":
        from macro_sync.exporters.netcdf_exporter import entries_to_netcdf_bytes, summaries_to_netcdf_bytes
        return summaries_to_netcdf_bytes(summaries) if use_summaries else entries_to_netcdf_bytes(entries)

    if fmt == "avro":
        from macro_sync.exporters.avro_exporter import entries_to_avro_bytes, summaries_to_avro_bytes
        return summaries_to_avro_bytes(summaries) if use_summaries else entries_to_avro_bytes(entries)

    raise ValueError(f"Unsupported export format: {fmt!r}")
