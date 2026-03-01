# Proven Service calculationComponents Formats

Each entry below has been tested and confirmed to produce a working, shareable
AWS Pricing Calculator URL. Use these as templates when building estimates.

**Tier 1 (fully editable in calculator):** EC2, EBS, Flink, S3, Secrets Manager
**Tier 2 (may show read-only warning):** AppStream, RDS Oracle, MSK, OpenSearch

---

## EC2 (Tier 1)

- **serviceCode:** `ec2Enhancement`
- **estimateFor:** `"template"`
- **Parameterizable:** instanceType, selectedOS, workload.data (instance count), pricingStrategy, storageType, storageAmount

```json
{
  "tenancy": {"value": "shared"},
  "selectedOS": {"value": "linux"},
  "workloadSelection": {"value": "consistent"},
  "workload": {
    "value": {
      "workloadType": "consistent",
      "data": "1"
    }
  },
  "instanceType": {"value": "t3.medium"},
  "pricingStrategy": {
    "value": {
      "selectedOption": "onDemand"
    }
  },
  "storageType": {"value": "Storage General Purpose gp3 GB Mo"},
  "storageAmount": {"value": "30", "unit": "gb"},
  "snapshotFrequency": {"value": "0"},
  "detailedMonitoringCheckbox": {"value": false},
  "ec2AdvancedPricingMetrics": {"value": 1},
  "dataTransferForEC2": {
    "value": [
      {"entryType": "INBOUND", "value": "", "unit": "tb_month", "fromRegion": ""},
      {"entryType": "OUTBOUND", "value": "", "unit": "tb_month", "toRegion": ""},
      {"entryType": "INTRA_REGION", "value": "", "unit": "tb_month"}
    ]
  }
}
```

**Pricing formula:** `instances * hourly_rate * 730`

---

## EBS (Tier 1)

- **serviceCode:** `amazonElasticBlockStore`
- **estimateFor:** `"elasticBlockStore"`
- **Parameterizable:** storageType, storageAmount, iops

```json
{
  "numberOfInstances": {"value": "1"},
  "durationOfInstanceRuns": {"value": "730", "unit": "hours"},
  "storageType": {"value": "Storage Provisioned IOPS GB Mo"},
  "storageAmount": {"value": "1400", "unit": "gb|NA"},
  "iops": {"value": "3000"},
  "snapshotFrequency": {"value": "0"},
  "snapshotAmount": {"value": "0", "unit": "gb|NA"}
}
```

**Pricing formula:** `(gb * storage_rate) + (iops * iops_rate)`

For gp3: use `"storageType": {"value": "Storage General Purpose gp3 GB Mo"}`

---

## Apache Flink (Tier 1)

- **serviceCode:** `amazonKinesisDataAnalytics`
- **estimateFor:** `"template"`
- **Parameterizable:** numberOfFlinkApps, numberOfFlinkKPU, numberOfBackups, appBackupSize

```json
{
  "numberOfFlinkApps": {"value": "1"},
  "numberOfFlinkKPU": {"value": "4", "unit": "perHour"},
  "numberOfBackups": {"value": "1"},
  "appBackupSize": {"value": "1", "unit": "gb"},
  "numberOfStudioApps": {"value": "0"},
  "numberOfStudioKPU": {"value": "0", "unit": "perHour"}
}
```

**Pricing formula:** `(kpus * kpu_hourly * 730) + (backup_gb * backup_rate)`

---

## S3 (Tier 1)

- **serviceCode:** `amazonS3`
- **estimateFor:** `"template_0"`
- **Parameterizable:** storage (gb), PUT requests, GET requests

```json
{
  "s3Services_generated_0": {"value": "10", "unit": "gb"},
  "s3Services_generated_1": {"value": "10000"},
  "s3Services_generated_2": {"value": "100000"},
  "s3Services_generated_3": {"value": "0", "unit": "gb"}
}
```

Fields: `_0` = storage GB, `_1` = PUT/COPY/POST requests, `_2` = GET/SELECT requests, `_3` = data returned by S3 Select

**Pricing formula:** `(gb * storage_rate) + (puts/1000 * put_rate) + (gets/1000 * get_rate)`

---

## Secrets Manager (Tier 1)

- **serviceCode:** `awsSecretsManager`
- **estimateFor:** `"awssecretsmanager"`
- **Parameterizable:** NumberOfSecrets, numberOfAPIs

```json
{
  "NumberOfSecrets": {"value": "2"},
  "secretDuration": {"value": "730"},
  "numberOfAPIs": {"value": "10000", "unit": "perMonth"}
}
```

**Pricing formula:** `(secrets * per_secret_rate) + (api_calls/10000 * per_10k_rate)`

---

## AppStream (Tier 2)

- **serviceCode:** `amazonAppStream`
- **estimateFor:** `"appStream2"`
- **Note:** Uses `columnFormIPM` — may trigger read-only warning

```json
{
  "appStreamFleet_instancePriceModel": {"value": "730"},
  "appStream_numberOfWorkingHours": {"value": "24"},
  "percentBuffer": {"value": "0"},
  "appStream_instanceDiskVolumeSizeGB": {"value": "200"},
  "columnFormIPM": {
    "value": [
      {
        "Instance Type": {"value": "stream.standard.xlarge"},
        "Operating System": {"value": "Windows"},
        "Multi Session": {"value": "True"}
      }
    ]
  },
  "appStream_licenseModel": {
    "value": "User Fees Windows AppStream provided per users"
  },
  "numberPicker": {"value": "0"},
  "appStream_numberOfUsers": {"value": "7"},
  "appStream_numberofsession": {"value": "7"},
  "daysInWD": {"value": "5"},
  "appStreamFleet_utilization1": {"value": "24"},
  "daysInWE": {"value": "2"},
  "appStreamFleet_utilization2": {"value": "24"},
  "baselineUsersPerHourWD": {"value": "7"},
  "peakUsersPerHourWD": {"value": "7"},
  "baselineUsersPerHourWE": {"value": "7"},
  "peakUsersPerHourWE": {"value": "7"}
}
```

**Pricing formula:** `instances * hourly_rate * 730` (Always-On = 730 hrs)

---

## RDS Oracle (Tier 2)

- **serviceCode:** `amazonRdsForOracle`
- **estimateFor:** `"rdsForOracle"`
- **Note:** Uses `columnFormIPM` — may trigger read-only warning

```json
{
  "columnFormIPM": {
    "value": [
      {
        "Number of Nodes": {"value": "1"},
        "Instance Type": {"value": "db.m5.xlarge"},
        "undefined": {
          "value": {
            "unit": "100",
            "selectedId": "%Utilized/Month"
          }
        },
        "Deployment Option": {"value": "Single-AZ"},
        "TermType": {"value": "OnDemand"},
        "License Model": {"value": "License included"},
        "Database Edition": {"value": "Standard Edition Two"}
      }
    ]
  },
  "storageType": {"value": "Provisioned IOPS"},
  "storageAmount": {"value": "800", "unit": "gb|NA"},
  "provisioningIOPS": {"value": "3000"},
  "DatabaseInsightsSelected": {"value": "0"},
  "retentionPeriod": {"value": "0"}
}
```

**Pricing formula:** `(nodes * hourly * 730) + (gb * storage_rate) + (iops * iops_rate)`

---

## MSK (Tier 2)

- **serviceCode:** `amazonManagedStreamingForApacheKafkaMsk`
- **estimateFor:** `"amazonMSK"`
- **Note:** Uses `columnFormIPM` — may trigger read-only warning

```json
{
  "columnFormIPM": {
    "value": [
      {
        "Number of Kafka broker nodes": {"value": "3"},
        "Compute Family": {"value": "kafka.m5.large"}
      }
    ]
  },
  "msk_storageAmount": {"value": "100", "unit": "gb"},
  "numberOfPrivateConnHours": {"value": "1"},
  "dataProcessedForPrivateConn": {"value": "100", "unit": "gb"},
  "averageDataIngressed": {"value": "5", "unit": "mbps"},
  "averageDataEgressed": {"value": "10", "unit": "mbps"},
  "totalPartitions": {"value": "100"},
  "MSK_Serverless_dataretention": {"value": "24"},
  "Number_of_MCUs": {"value": "0"}
}
```

**Pricing formula:** `(brokers * hourly * 730) + (brokers * storage_gb * storage_rate) + private_connectivity`

---

## OpenSearch (Tier 2)

- **serviceCode:** `amazonElasticsearchService`
- **estimateFor:** `"elasticSearchService"`
- **Note:** Uses `columnFormIPM_1` — may trigger read-only warning

```json
{
  "columnFormIPM_1": {
    "value": [
      {
        "Number of Nodes Data instance": {"value": "2"},
        "Instance Type": {"value": "r5.large.search"},
        "undefined": {
          "value": {
            "unit": "100",
            "selectedId": "%Utilized/Month"
          }
        },
        "Instance Family": {"value": "Standard Instances - Current Generation"},
        "TermType": {"value": "OnDemand"}
      }
    ]
  },
  "numberOfInstances": {"value": "2"},
  "storageType": {"value": "GP3"},
  "gp3StorageAmount": {"value": "100", "unit": "gb"},
  "gp3ProvisioningIOPS": {"value": "3000"},
  "gp3Throughput": {"value": "125", "unit": "mbps"}
}
```

**Pricing formula:** `(nodes * hourly * 730) + (nodes * storage_gb * storage_rate)`
