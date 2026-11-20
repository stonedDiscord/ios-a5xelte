/* SC2730 retained UTC, using the live SM-A035G DT and stock rtc-sc27xx
 * register layout. No RTC, alarm, reset or PMIC configuration writes.
 * Caller holds the shared ADI lock. Read commands use existing adi_read. */
static int
a03_rtc_snapshot(uint64_t *utc)
{
 uint32_t power, after, sec, min, hour, day;
 uint64_t previous = 0;
 int have_previous = 0;
 for (unsigned attempt = 0; attempt < 4; attempt++) {
  if (!adi_read(0x25c, &power) || power == 0x96 ||
      !adi_read(0x20c, &day) || !adi_read(0x208, &hour) ||
      !adi_read(0x204, &min) || !adi_read(0x200, &sec) ||
      !adi_read(0x25c, &after) || power != after) return 0;
  /* Reject corrupt/reserved bits rather than mask them into a date. */
  if (sec > 59 || min > 59 || hour > 23 || day > 65535) return 0;
  uint64_t value = (((uint64_t)day * 24 + hour) * 60 + min) * 60 + sec;
  if (value < 1577836800ULL || value > 4102444799ULL) return 0;
  /* Two identical complete samples reject mixed fields during rollover. */
  if (have_previous && previous == value) { *utc = value; return 1; }
  previous = value; have_previous = 1;
 }
 return 0;
}
