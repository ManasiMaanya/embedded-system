#pragma once

// L3 constants — docs/mathematics.md equations (4)–(5) and H.
// Keep sim/adaptive_threshold.py identical.

constexpr int kAvgSamples = 32;       // M
constexpr int kHyst = 40;             // H, counts
constexpr float kVmaxKmh = 120.0f;
constexpr float kAdcMax = 4095.0f;

constexpr float kTmod0 = 180.0f;      // T_MOD,0  counts
constexpr float kKmod = 0.8f;         // K_MOD    counts / (km/h)
constexpr float kThigh0 = 420.0f;     // T_HIGH,0
constexpr float kKhigh = 1.2f;        // K_HIGH
