# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.13.0] - 2024-05-30
This is the first release of this project under Gravitational management.

### Added

- Helm chart with Prometheus Operator support, pushed to GHCR [#29](https://github.com/gravitational/aws-quota-checker/pull/29)
- Multiarch container images [#33](https://github.com/gravitational/aws-quota-checker/pull/33)
- Images are now also pushed to GHCR, and include semver tags [#28](https://github.com/gravitational/aws-quota-checker/pull/28)
- Quota limits are now overridable via the `--limit-override` parameter [#31](https://github.com/gravitational/aws-quota-checker/pull/31)
- Service quota lookups are now cached [#22](https://github.com/gravitational/aws-quota-checker/pull/22)
- Added SNS checks for messages published per second, topic transactions per second,
  and resource transactions per second [#23](https://github.com/gravitational/aws-quota-checker/pull/23)
- A new dynamic dashboard has been added to visualize resources nearing their
  quota limits [#29](https://github.com/gravitational/aws-quota-checker/pull/29)
- Added checks for KMS, Athena, EKS, and EC2 launch templates [#15](https://github.com/gravitational/aws-quota-checker/pull/15)
- Added VPC checks for endpoint count, NAT gateway count, and peering
  connections per VPC [#6](https://github.com/gravitational/aws-quota-checker/pull/6)

### Changed

- The `instance` label is now called `aws_resource` to avoid naming conflict
  with Prometheus' `instance` service discovery label [#35](https://github.com/gravitational/aws-quota-checker/pull/35)
- Updated dependencies
- Request duration metrics will now also include `account`, `region`, and
  `aws_resource` labels [#34](https://github.com/gravitational/aws-quota-checker/pull/34)
- Updated all quota descriptions to match AWS descriptions [#20](https://github.com/gravitational/aws-quota-checker/pull/20)

### Fixed
- Fixed assorted quota scopes using incorrect values [#21](https://github.com/gravitational/aws-quota-checker/pull/21)

## [1.12.0] - 2022-01-14

### Added

- new check: rds_cluster_snapshots
- new check: rds_instance_snapshots

## [1.11.0] - 2022-01-10

### Changed

- improve EBS snapshot count check by using paginated requests

## [1.10.0] - 2022-01-06

### Added

- add error handling for CLI result reporter
- new check: iam_role_count
- Prometheus metrics now have a new label that contains the quota key, see [#31](https://github.com/brennerm/aws-quota-checker/issues/31) for further details

## [1.9.0] - 2021-09-21

### Added

- new check: rds_event_subscriptions

### Removed

- obsolete check: cw_alarm_count

## [1.8.0] - 2021-09-10

### Added

- new check: rds_instances
- new check: rds_parameter_groups
- new check: rds_cluster_parameter_groups

### Fixed

- iterator bug that prevented check-instance command to function

### Security

- update several dependencies

## [1.7.0] - 2021-05-05

### Added

- new check: lambda_function_storage

## [1.6.0] - 2021-04-30

### Added

- new check: elb_target_groups_per_alb

### Fixed

- fix wrong number of EBS snapshots

## [1.5.0] - 2021-04-19

### Added

- new check: ses_daily_sends

### Fixed

- upgraded urllib due to [vulnerability CVE-2021-28363](https://github.com/advisories/GHSA-5phf-pp7p-vc2r)

## [1.4.1] - 2021-03-25

### Fixed

- make code compatible with Python 3.7

## [1.4.0] - 2021-03-21

### Added

- new check: vpc_rules_per_acl
- new check: vpc_ipv4_cidr_blocks_per_vpc
- new check: vpc_ipv6_cidr_blocks_per_vpc
- new check: vpc_rules_per_sg
- new check: vpc_route_tables_per_vpc
- new check: vpc_routes_per_route_table
- add Grafana dashboard: on-demand-ec2
- new Prometheus metric that will expose the time it took to get the current/max value of each check

## [1.3.1] - 2021-03-17

### Fixed

- fix check key validation for _check_ and _prometheus-exporter_ subcommands

## [1.3.0] - 2021-03-12

### Added

- now available as a Docker image, give it a try with `docker run ghcr.io/brennerm/aws-quota-checker:latest`
- improve autocompletion support

## [1.2.0] - 2021-03-09

### Added

- implement Prometheus exporter that provides access to all quota results

### Changed

- display AWS account ID instead of profile name in check scope

## [1.1.0] - 2021-02-27

### Added

- new check: ec2_on_demand_f_count
- new check: ec2_on_demand_g_count
- new check: ec2_on_demand_p_count
- new check: ec2_on_demand_x_count
- new check: ec2_on_demand_inf_count
- new check: ec2_spot_f_count
- new check: ec2_spot_g_count
- new check: ec2_spot_p_count
- new check: ec2_spot_x_count
- new check: ec2_spot_inf_count
- new check: sns_topics_count
- new check: sns_pending_subscriptions_count
- new check: sns_subscriptions_per_topic

### Changed

- sort checks alphabetically by key

## [1.0.0] - 2021-02-24

### Added

- initial release
