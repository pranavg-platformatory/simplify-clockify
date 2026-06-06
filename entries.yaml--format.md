<h1><code>entries.yaml</code> Format</h1>

> **The YAML file in question**: [`entries.yaml`](./entries.yaml)

---

The object represented by `entries.yaml` is a list of maps; each map contains:

- `startDate` mapped to a date string in the format: `YY-mm-dd` (e.g. 2025-12-31) (**string**)
- `startTime` mapped to a time string in the format: `HH:MM` (24 hour clock) (**string**)
- `tasks` mapped to an array of maps; each map contains:
    - `description` mapped to task description (**string**)
    - `timeTaken` mapped to time taken in hours (**float**; decimals are acceptable)
    - `projectName` mapped to a project name (**string**)
    - `billable` mapped to a true/false value (**boolean**)

For clarity, this is how these fields would be arranged in YAML:

```yaml
- startDate: ... # format: YYYY-mm-dd
  startTime: ... # format: HH:mm (24 hour clock)
  tasks:
    - description: ... # can be left empty as well
      timeTaken: ...   # only in hours; decimals are acceptable; defaults to 1 hour
      projectName: ... # defaults to FDH-PH
      billable: ...    # defaults to false
```

E.g.:

```yaml
- startDate: '2026-06-06'
  startTime: '05:50'
  tasks:
    - description: awesome task
      timeTaken: 2
      projectName: FDH-NA
      billable: false
    - description: amazing task
      timeTaken: 1
      projectName: FDH-PH
      billable: false

--- # <- This divider is optional of course
- startDate: '2026-06-07'
  startTime: '06:43'
  tasks:
    - description: awesome task
      timeTaken: 2
      projectName: FDH-NA
      billable: false
    - description: dumb task
      timeTaken: 5
      projectName: FDH-NA
      billable: false
    - description: super task
      timeTaken: 1.2
      projectName: FDH-PH
      billable: false
```