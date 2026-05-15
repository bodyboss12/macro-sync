"""Unified export dispatcher for macro-sync."""
from __future__ import annotations

from typing import List, Union

from macro_sync.schema import DailySummary, NutritionEntry

Data = Union[List[NutritionEntry], List[DailySummary]]


def export(data: Data, fmt: str) -> Union[str, bytes]:
    """Export *data* in the requested format.

    Parameters
    ----------
    data:
        A list of NutritionEntry or DailySummary objects.
    fmt:
        Target format string, e.g. ``"json"``, ``"csv"``, ``"hdf5"``.

    Returns
    -------
    str or bytes depending on the format.
    """
    is_summary = data and isinstance(data[0], DailySummary)

    if fmt == "json":
        from macro_sync.exporters.json_exporter import summaries_to_json_str, entries_to_json_str
        return summaries_to_json_str(data) if is_summary else entries_to_json_str(data)  # type: ignore[arg-type]
    if fmt == "csv":
        from macro_sync.exporters.csv_exporter import summaries_to_csv_str, entries_to_csv_str
        return summaries_to_csv_str(data) if is_summary else entries_to_csv_str(data)  # type: ignore[arg-type]
    if fmt == "tsv":
        from macro_sync.exporters.tsv_exporter import summaries_to_tsv_str, entries_to_tsv_str
        return summaries_to_tsv_str(data) if is_summary else entries_to_tsv_str(data)  # type: ignore[arg-type]
    if fmt == "markdown":
        from macro_sync.exporters.markdown_exporter import summaries_to_markdown_str, entries_to_markdown_str
        return summaries_to_markdown_str(data) if is_summary else entries_to_markdown_str(data)  # type: ignore[arg-type]
    if fmt == "html":
        from macro_sync.exporters.html_exporter import summaries_to_html_str, entries_to_html_str
        return summaries_to_html_str(data) if is_summary else entries_to_html_str(data)  # type: ignore[arg-type]
    if fmt == "xml":
        from macro_sync.exporters.xml_exporter import summaries_to_xml_str, entries_to_xml_str
        return summaries_to_xml_str(data) if is_summary else entries_to_xml_str(data)  # type: ignore[arg-type]
    if fmt == "yaml":
        from macro_sync.exporters.yaml_exporter import summaries_to_yaml_str, entries_to_yaml_str
        return summaries_to_yaml_str(data) if is_summary else entries_to_yaml_str(data)  # type: ignore[arg-type]
    if fmt == "toml":
        from macro_sync.exporters.toml_exporter import summaries_to_toml_str, entries_to_toml_str
        return summaries_to_toml_str(data) if is_summary else entries_to_toml_str(data)  # type: ignore[arg-type]
    if fmt == "latex":
        from macro_sync.exporters.latex_exporter import summaries_to_latex_str, entries_to_latex_str
        return summaries_to_latex_str(data) if is_summary else entries_to_latex_str(data)  # type: ignore[arg-type]
    if fmt == "ndjson":
        from macro_sync.exporters.ndjson_exporter import summaries_to_ndjson_str, entries_to_ndjson_str
        return summaries_to_ndjson_str(data) if is_summary else entries_to_ndjson_str(data)  # type: ignore[arg-type]
    if fmt == "jsonl":
        from macro_sync.exporters.jsonl_exporter import summaries_to_jsonl_str, entries_to_jsonl_str
        return summaries_to_jsonl_str(data) if is_summary else entries_to_jsonl_str(data)  # type: ignore[arg-type]
    if fmt == "excel":
        from macro_sync.exporters.excel_exporter import summaries_to_excel_bytes, entries_to_excel_bytes
        return summaries_to_excel_bytes(data) if is_summary else entries_to_excel_bytes(data)  # type: ignore[arg-type]
    if fmt == "parquet":
        from macro_sync.exporters.parquet_exporter import summaries_to_parquet_bytes, entries_to_parquet_bytes
        return summaries_to_parquet_bytes(data) if is_summary else entries_to_parquet_bytes(data)  # type: ignore[arg-type]
    if fmt == "arrow":
        from macro_sync.exporters.arrow_exporter import summaries_to_arrow_bytes, entries_to_arrow_bytes
        return summaries_to_arrow_bytes(data) if is_summary else entries_to_arrow_bytes(data)  # type: ignore[arg-type]
    if fmt == "feather":
        from macro_sync.exporters.feather_exporter import summaries_to_feather_bytes, entries_to_feather_bytes
        return summaries_to_feather_bytes(data) if is_summary else entries_to_feather_bytes(data)  # type: ignore[arg-type]
    if fmt == "msgpack":
        from macro_sync.exporters.msgpack_exporter import summaries_to_msgpack_bytes, entries_to_msgpack_bytes
        return summaries_to_msgpack_bytes(data) if is_summary else entries_to_msgpack_bytes(data)  # type: ignore[arg-type]
    if fmt == "sqlite":
        from macro_sync.exporters.sqlite_exporter import summaries_to_sqlite_bytes, entries_to_sqlite_bytes
        return summaries_to_sqlite_bytes(data) if is_summary else entries_to_sqlite_bytes(data)  # type: ignore[arg-type]
    if fmt == "pdf":
        from macro_sync.exporters.pdf_exporter import summaries_to_pdf_bytes, entries_to_pdf_bytes
        return summaries_to_pdf_bytes(data) if is_summary else entries_to_pdf_bytes(data)  # type: ignore[arg-type]
    if fmt == "ods":
        from macro_sync.exporters.ods_exporter import summaries_to_ods_bytes, entries_to_ods_bytes
        return summaries_to_ods_bytes(data) if is_summary else entries_to_ods_bytes(data)  # type: ignore[arg-type]
    if fmt == "netcdf":
        from macro_sync.exporters.netcdf_exporter import summaries_to_netcdf_bytes, entries_to_netcdf_bytes
        return summaries_to_netcdf_bytes(data) if is_summary else entries_to_netcdf_bytes(data)  # type: ignore[arg-type]
    if fmt == "hdf5":
        from macro_sync.exporters.hdf5_exporter import summaries_to_hdf5_bytes, entries_to_hdf5_bytes
        return summaries_to_hdf5_bytes(data) if is_summary else entries_to_hdf5_bytes(data)  # type: ignore[arg-type]
    raise ValueError(f"Unsupported export format: {fmt!r}")
