# TradeBytes

**Unofficial Nasdaq and Barchart Data API**

---

⚠️ **Important Legal Disclaimer** ⚠️

TradeBytes is not affiliated with, endorsed by, or vetted by Nasdaq or Barchart, Inc. This is an open-source project designed for research and educational purposes only. It interacts with publicly available APIs provided by Nasdaq and Barchart. Use of this tool is subject to the terms and conditions of these platforms. Users are advised to consult the respective platforms for discrepancies or data validation.

---

## Overview

TradeBytes is a lightweight Python-based library that simplifies the process of fetching and analyzing market data using publicly available APIs from Barchart and (soon) Nasdaq. Whether you’re a researcher, developer, or hobbyist, TradeBytes provides an easy-to-use interface for querying complex market data structures, such as options spreads and strategies.

### Key Features:
- **Predefined API Integrations**: Includes support for a wide range of options strategies and market data APIs.
- **Customizable Output**: Save results in JSON format for easy processing.
- **Extensible Design**: Built to support additional APIs and providers in the future.
- **Open-Source Collaboration**: Contributions are welcome!

---

## Supported Features

### Barchart API

TradeBytes supports querying the following data from Barchart:

| **Category**             | **Available APIs**                                                                                          |
|---------------------------|------------------------------------------------------------------------------------------------------------|
| **Condors**              | `long_call_condors`, `short_call_condors`, `long_put_condors`, `short_put_condors`                          |
| **Iron Condors**         | `long_iron_condors`, `short_iron_condors`                                                                   |
| **Butterfly Spreads**    | `short_iron_butterfly_spread`, `long_iron_butterfly_spread`, `short_put_butterfly_spread`, `long_put_butterfly_spread`, `short_call_butterfly_spread`, `long_call_butterfly_spread` |
| **Strangles & Straddles**| `short_strangle_spread`, `long_strangle_spread`, `short_straddle_spread`, `long_straddle_spread`            |
| **Diagonal Spreads**     | `bull_puts_diagonal_spread`, `bear_puts_diagonal_spread`, `bear_calls_diagonal_spread`, `bull_calls_diagonal_spread` |
| **Calendar Spreads**     | `long_put_calendar_spread`, `long_call_calendar_spread`                                                    |
| **Collars & Married Puts**| `long_collar_spread`, `married_put`                                                                        |
| **Vertical Spreads**     | `bull_puts_spread`, `bear_puts_spread`, `bear_calls_spread`, `bull_calls_spread`                            |
| **Single-Leg Strategies**| `naked_puts`, `covered_calls`                                                                              |

> **Note:** The free version of Barchart limits queries to 10,000 rows of data. This restriction is imposed by Barchart and applies regardless of the API or strategy being queried.

---

## Installation & Usage

### 1. Listing Available APIs

To see all supported APIs, run the following command:

```bash
python3 -m src.main --provider barchart --api list

Example Output:

INFO:__main__:Available APIs:
- long_call_condors
- short_call_condors
- long_put_condors
...

2. Querying Data for an API

To fetch data for a specific API, use the following command:

python3 -m src.main --provider barchart --api <api_name> --output <output_file>

Example:

python3 -m src.main --provider barchart --api long_call_condors --output long_call_condors_data.json

This will save the fetched data in long_call_condors_data.json.

3. Configuring the Tool

Configurations for Barchart APIs are defined in config/barchart_apis.json. You can customize query parameters, headers, and other settings as needed.

Future Plans

TradeBytes is actively evolving. Here are some planned features:
	1.	Nasdaq API Integration: Support for Nasdaq market data is on the roadmap.
	2.	Expanded Features: Include advanced analytics and visualization tools.
	3.	Custom Query Support: Enable users to define custom strategies and queries.
	4.	Documentation and Examples: Provide more examples, tutorials, and detailed usage guides.

Contributing

We welcome contributions to make TradeBytes better! Here’s how you can contribute:
	•	Add support for new APIs.
	•	Report and fix bugs.
	•	Improve documentation and examples.
	•	Suggest new features or enhancements.

To Get Started:
	1.	Fork the repository.
	2.	Make your changes.
	3.	Submit a pull request with a detailed description.

Support

For any discrepancies in the data, please visit the Barchart Options Website.

If you encounter issues with TradeBytes or have feature requests, please open an issue on GitHub.

License

TradeBytes is released under the MIT License.

Happy Trading! 🚀

