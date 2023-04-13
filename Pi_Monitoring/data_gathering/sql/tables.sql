-- metrics definition

CREATE TABLE `metrics` (
  `hostname` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `cpu_percent` float DEFAULT NULL,
  `cpu_temp` float DEFAULT NULL,
  `ram_percent` float DEFAULT NULL,
  `ram_available_mbyte` decimal(10,2) DEFAULT NULL,
  `ram_used_mbyte` decimal(10,2) DEFAULT NULL,
  `ram_swap_percent` float DEFAULT NULL,
  `disk_percent` float DEFAULT NULL,
  `disk_used_mbyte` decimal(10,2) DEFAULT NULL,
  `disk_free_mbyte` decimal(10,2) DEFAULT NULL,
  `net_sent_gbyte` decimal(10,2) DEFAULT NULL,
  `net_received_gbyte` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;