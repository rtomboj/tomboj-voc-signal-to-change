/** Table-reader boundary: preserve unknowns, serialize native Date cells before freshness logic. */
function vocMonitorCell_(value, timezone) {
  if (value instanceof Date) {
    return isNaN(value.getTime()) ? '' : Utilities.formatDate(value, timezone, "yyyy-MM-dd'T'HH:mm:ssXXX");
  }
  return value == null ? '' : value;
}

/** Call on getValues() rows with the actual workbook timezone, before mapping headers or slicing text. */
function vocMonitorTableValues_(rows, timezone) {
  return rows.map(function (row) {
    return row.map(function (value) { return vocMonitorCell_(value, timezone); });
  });
}
