-- metrics definition

CREATE TABLE `metrics` (
  `hostname` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `cpu_percent` float DEFAULT NULL,
  `cpu_temp` float DEFAULT NULL,
  `ram_percent` float DEFAULT NULL,
  `ram_available` bigint(20) DEFAULT NULL,
  `ram_used` bigint(20) DEFAULT NULL,
  `ram_swap_percent` float DEFAULT NULL,
  `disk_percent` float DEFAULT NULL,
  `disk_used` bigint(20) DEFAULT NULL,
  `disk_free` bigint(20) DEFAULT NULL,
  `net_sent` bigint(20) DEFAULT NULL,
  `net_received` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

