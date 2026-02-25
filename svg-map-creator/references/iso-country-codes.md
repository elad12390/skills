# ISO Country Codes and Map Region Identifiers

Sources: ISO 3166-1 standard, SimpleMaps SVG convention analysis, Natural Earth Data

Covers: complete ISO 3166-1 alpha-2 country code table, SimpleMaps id vs class mapping, multi-path country list, US state codes, special territories handling, disputed regions.

## 1. SimpleMaps ID Convention Summary

SimpleMaps uses a specific naming convention in their SVG files to identify regions. Understanding these attributes is critical for automated manipulation:

*   **Most Countries**: Identified via the `id` attribute using the ISO 3166-1 alpha-2 code in uppercase (e.g., `id="FR"` for France).
*   **Multi-path Countries**: Countries composed of multiple distinct geographical areas (exclaves, islands) often lack an `id` on individual `<path>` elements. Instead, they share a `class` attribute named after the country (e.g., `class="Canada"`).
*   **Non-Standard Codes**: SimpleMaps uses custom 4-letter codes for certain sub-territories of the Netherlands to differentiate them in the world map (e.g., `BQBO` for Bonaire).
*   **Precedence**: When searching for a country, always check for the `id` first. If no ID matches, search for the `class` attribute using the SimpleMaps standard name.
*   **Targeting Strategy**: To highlight a country like Australia, the agent must target both the path with `id="AU"` (if it exists) and all paths with `class="Australia"`.

## 2. Multi-Path Countries (CRITICAL TABLE)

These countries require special handling because they are represented by multiple SVG paths. Using `getElementById` will only return the first path; a class-based selector or a query for all elements with the matching class is necessary.

| Class Name | ISO Code | Reason for Multi-Path Representation |
| :--- | :--- | :--- |
| Angola | AO | Includes the Cabinda exclave separated by the DRC |
| Argentina | AR | Includes Mainland and the Tierra del Fuego archipelago |
| Australia | AU | Includes the Mainland, Tasmania, and smaller islands |
| Azerbaijan | AZ | Includes Mainland and the Nakhchivan exclave |
| Canada | CA | Mainland plus a vast number of Arctic islands and archipelagos |
| China | CN | Includes Mainland, Hainan, and grouped Taiwan area regions |
| Denmark | DK | Includes the Jutland peninsula and numerous Baltic islands |
| Greece | GR | Includes the Balkan mainland and thousands of Aegean/Ionian islands |
| United Kingdom | GB | Grouping of England, Wales, Scotland, and Northern Ireland paths |
| United States | US | Includes Mainland, Alaska, and Hawaii (in world.svg) |
| France | FR | Includes Mainland and Corsica (often separate paths) |
| Italy | IT | Includes Mainland, Sicily, and Sardinia |
| Japan | JP | Archipelago consisting of Honshu, Hokkaido, Kyushu, Shikoku, etc. |
| Malaysia | MY | Split between Peninsular Malaysia and East Malaysia (Borneo) |
| Norway | NO | Extremely fragmented coastline with numerous coastal islands |
| Russia | RU | Vast territory including the Kaliningrad exclave |

## 3. Complete ISO 3166-1 Alpha-2 Code Table

The following table provides the mapping used in the `world.svg` file.

| Code | Country | Notes |
| :--- | :--- | :--- |
| AE | United Arab Emirates | Standard ID |
| AF | Afghanistan | Standard ID |
| AI | Anguilla | Standard ID |
| AL | Albania | Standard ID |
| AM | Armenia | Standard ID |
| AO | Angola | Multi-path; use class="Angola" |
| AR | Argentina | Multi-path; use class="Argentina" |
| AT | Austria | Standard ID |
| AU | Australia | Multi-path; use class="Australia" |
| AW | Aruba | Standard ID |
| AZ | Azerbaijan | Multi-path; use class="Azerbaijan" |
| BA | Bosnia and Herzegovina | Standard ID |
| BB | Barbados | Standard ID |
| BD | Bangladesh | Standard ID |
| BE | Belgium | Standard ID |
| BF | Burkina Faso | Standard ID |
| BG | Bulgaria | Standard ID |
| BH | Bahrain | Standard ID |
| BI | Burundi | Standard ID |
| BJ | Benin | Standard ID |
| BL | Saint-Barthelemy | Standard ID |
| BM | Bermuda | Standard ID |
| BN | Brunei Darussalam | Standard ID |
| BO | Bolivia | Standard ID |
| BQBO | Netherlands (Bonaire) | Custom SimpleMaps code |
| BQSA | Saba (Netherlands) | Custom SimpleMaps code |
| BQSE | St. Eustatius (Netherlands) | Custom SimpleMaps code |
| BR | Brazil | Standard ID |
| BT | Bhutan | Standard ID |
| BW | Botswana | Standard ID |
| BY | Belarus | Standard ID |
| BZ | Belize | Standard ID |
| CA | Canada | Multi-path; use class="Canada" |
| CD | Democratic Republic of the Congo | Standard ID |
| CF | Central African Republic | Standard ID |
| CG | Republic of Congo | Standard ID |
| CH | Switzerland | Standard ID |
| CI | Cote d'Ivoire | Standard ID |
| CM | Cameroon | Standard ID |
| CN | China | Multi-path; use class="China" |
| CO | Colombia | Standard ID |
| CR | Costa Rica | Standard ID |
| CU | Cuba | Standard ID |
| CW | Curacao | Standard ID |
| CZ | Czech Republic | Standard ID |
| DE | Germany | Standard ID |
| DJ | Djibouti | Standard ID |
| DK | Denmark | Multi-path; use class="Denmark" |
| DM | Dominica | Standard ID |
| DO | Dominican Republic | Standard ID |
| DZ | Algeria | Standard ID |
| EC | Ecuador | Standard ID |
| EE | Estonia | Standard ID |
| EG | Egypt | Standard ID |
| EH | Western Sahara | Disputed territory; standard ID |
| ER | Eritrea | Standard ID |
| ES | Spain | Standard ID |
| ET | Ethiopia | Standard ID |
| FI | Finland | Standard ID |
| GA | Gabon | Standard ID |
| GB | United Kingdom | Multi-path; use class="United Kingdom" |
| GD | Grenada | Standard ID |
| GE | Georgia | Standard ID |
| GF | French Guiana | Standard ID |
| GH | Ghana | Standard ID |
| GL | Greenland | Standard ID |
| GM | The Gambia | Standard ID |
| GN | Guinea | Standard ID |
| GQ | Equatorial Guinea | Standard ID |
| GR | Greece | Multi-path; use class="Greece" |
| GT | Guatemala | Standard ID |
| GU | Guam | Standard ID |
| GW | Guinea-Bissau | Standard ID |
| GY | Guyana | Standard ID |
| HN | Honduras | Standard ID |
| HR | Croatia | Standard ID |
| HT | Haiti | Standard ID |
| HU | Hungary | Standard ID |
| IS | Iceland | Standard ID |
| IN | India | Standard ID |
| IR | Iran | Standard ID |
| IQ | Iraq | Standard ID |
| IE | Ireland | Standard ID |
| IL | Israel | Standard ID |
| JM | Jamaica | Standard ID |
| JO | Jordan | Standard ID |
| KZ | Kazakhstan | Standard ID |
| KE | Kenya | Standard ID |
| XK | Kosovo | Non-ISO; standard mapping in SimpleMaps |
| KW | Kuwait | Standard ID |
| KG | Kyrgyzstan | Standard ID |
| LA | Lao PDR | Standard ID |
| LV | Latvia | Standard ID |
| LB | Lebanon | Standard ID |
| LS | Lesotho | Standard ID |
| LR | Liberia | Standard ID |
| LY | Libya | Standard ID |
| LT | Lithuania | Standard ID |
| LU | Luxembourg | Standard ID |
| MK | Macedonia | Standard ID |
| MG | Madagascar | Standard ID |
| MW | Malawi | Standard ID |
| MV | Maldives | Standard ID |
| ML | Mali | Standard ID |
| MH | Marshall Islands | Standard ID |
| MQ | Martinique | Standard ID |
| MR | Mauritania | Standard ID |
| YT | Mayotte | Standard ID |
| MX | Mexico | Standard ID |
| MD | Moldova | Standard ID |
| MN | Mongolia | Standard ID |
| ME | Montenegro | Standard ID |
| MS | Montserrat | Standard ID |
| MA | Morocco | Standard ID |
| MZ | Mozambique | Standard ID |
| MM | Myanmar | Standard ID |
| NA | Namibia | Standard ID |
| NR | Nauru | Standard ID |
| NP | Nepal | Standard ID |
| NL | Netherlands | Standard ID |
| NI | Nicaragua | Standard ID |
| NE | Niger | Standard ID |
| NG | Nigeria | Standard ID |
| PK | Pakistan | Standard ID |
| PW | Palau | Standard ID |
| PS | Palestine | Standard ID |
| PA | Panama | Standard ID |
| PY | Paraguay | Standard ID |
| PE | Peru | Standard ID |
| PL | Poland | Standard ID |
| PT | Portugal | Standard ID |
| QA | Qatar | Standard ID |
| CG | Republic of Congo | Standard ID |
| KR | Republic of Korea | Standard ID |
| RE | Reunion | Standard ID |
| RO | Romania | Standard ID |
| RW | Rwanda | Standard ID |
| BQSA | Saba (Netherlands) | Custom SimpleMaps code |
| LC | Saint Lucia | Standard ID |
| VC | Saint Vincent and the Grenadines | Standard ID |
| BL | Saint-Barthelemy | Standard ID |
| MF | Saint-Martin | Standard ID |
| SA | Saudi Arabia | Standard ID |
| SN | Senegal | Standard ID |
| RS | Serbia | Standard ID |
| SL | Sierra Leone | Standard ID |
| SX | Sint Maarten | Standard ID |
| SK | Slovakia | Standard ID |
| SI | Slovenia | Standard ID |
| SO | Somalia | Standard ID |
| ZA | South Africa | Standard ID |
| SS | South Sudan | Standard ID |
| ES | Spain | Standard ID |
| LK | Sri Lanka | Standard ID |
| BQSE | St. Eustatius (Netherlands) | Custom SimpleMaps code |
| SD | Sudan | Standard ID |
| SR | Suriname | Standard ID |
| SZ | Swaziland | Standard ID |
| SE | Sweden | Standard ID |
| CH | Switzerland | Standard ID |
| SY | Syria | Standard ID |
| TW | Taiwan | Standard ID |
| TJ | Tajikistan | Standard ID |
| TZ | Tanzania | Standard ID |
| TH | Thailand | Standard ID |
| GM | The Gambia | Standard ID |
| TL | Timor-Leste | Standard ID |
| TG | Togo | Standard ID |
| TN | Tunisia | Standard ID |
| TM | Turkmenistan | Standard ID |
| TV | Tuvalu | Standard ID |
| UG | Uganda | Standard ID |
| UA | Ukraine | Standard ID |
| UY | Uruguay | Standard ID |
| UZ | Uzbekistan | Standard ID |
| VE | Venezuela | Standard ID |
| VN | Vietnam | Standard ID |
| EH | Western Sahara | Standard ID |
| YE | Yemen | Standard ID |
| ZM | Zambia | Standard ID |
| ZW | Zimbabwe | Standard ID |

## 4. US State Codes (for us.svg)

SimpleMaps US SVG files use standard 2-letter postal abbreviations as the `id` attribute.

| Code | State Name | Notes |
| :--- | :--- | :--- |
| AL | Alabama | Standard ID |
| AK | Alaska | Standard ID |
| AZ | Arizona | Standard ID |
| AR | Arkansas | Standard ID |
| CA | California | Standard ID |
| CO | Colorado | Standard ID |
| CT | Connecticut | Standard ID |
| DE | Delaware | Standard ID |
| FL | Florida | Standard ID |
| GA | Georgia | Standard ID |
| HI | Hawaii | Standard ID |
| ID | Idaho | Standard ID |
| IL | Illinois | Standard ID |
| IN | Indiana | Standard ID |
| IA | Iowa | Standard ID |
| KS | Kansas | Standard ID |
| KY | Kentucky | Standard ID |
| LA | Louisiana | Standard ID |
| ME | Maine | Standard ID |
| MD | Maryland | Standard ID |
| MA | Massachusetts | Standard ID |
| MI | Michigan | Standard ID |
| MN | Minnesota | Standard ID |
| MS | Mississippi | Standard ID |
| MO | Missouri | Standard ID |
| MT | Montana | Standard ID |
| NE | Nebraska | Standard ID |
| NV | Nevada | Standard ID |
| NH | New Hampshire | Standard ID |
| NJ | New Jersey | Standard ID |
| NM | New Mexico | Standard ID |
| NY | New York | Standard ID |
| NC | North Carolina | Standard ID |
| ND | North Dakota | Standard ID |
| OH | Ohio | Standard ID |
| OK | Oklahoma | Standard ID |
| OR | Oregon | Standard ID |
| PA | Pennsylvania | Standard ID |
| RI | Rhode Island | Standard ID |
| SC | South Carolina | Standard ID |
| SD | South Dakota | Standard ID |
| TN | Tennessee | Standard ID |
| TX | Texas | Standard ID |
| UT | Utah | Standard ID |
| VT | Vermont | Standard ID |
| VA | Virginia | Standard ID |
| WA | Washington | Standard ID |
| WV | West Virginia | Standard ID |
| WI | Wisconsin | Standard ID |
| WY | Wyoming | Standard ID |
| DC | District of Columbia | Treated as a state-level region |

## 5. Special Territories and Non-Standard Codes

| Code | Territory | Notes |
| :--- | :--- | :--- |
| XK | Kosovo | Widely used identifier, despite missing from ISO 3166-1 |
| BQBO | Bonaire | SimpleMaps specific code for this Caribbean island |
| BQSA | Saba | SimpleMaps specific code for this Caribbean island |
| BQSE | St. Eustatius | SimpleMaps specific code for this Caribbean island |
| TW | Taiwan | Listed as a separate entity from China |
| PS | Palestine | Represents West Bank and Gaza regions |
| EH | Western Sahara | Represented as a distinct region |
| GL | Greenland | Autonomous territory of Denmark, but has its own ID |
| GF | French Guiana | Overseas department of France, usually has its own ID |
| PR | Puerto Rico | Often included in US or World maps with standard ID |

## 6. Common Name Mismatches

Agents should use this table to translate user-provided names into the names used within the SimpleMaps SVG `class` attributes.

| Common Name | SimpleMaps Name | Code |
| :--- | :--- | :--- |
| North Korea | Dem. Rep. Korea | KP |
| South Korea | Republic of Korea | KR |
| DRC / Congo-Kinshasa | Democratic Republic of the Congo | CD |
| Congo-Brazzaville | Republic of Congo | CG |
| Ivory Coast | Cote d'Ivoire | CI |
| Laos | Lao PDR | LA |
| Eswatini | Swaziland | SZ |
| North Macedonia | Macedonia | MK |
| Myanmar / Burma | Myanmar | MM |
| Czechia | Czech Republic | CZ |
| Gambia | The Gambia | GM |
| United Arab Emirates | United Arab Emirates | AE |
| Timor-Leste | Timor-Leste | TL |
| United Kingdom | United Kingdom | GB |
| United States | United States | US |

## 7. Mapping Strategies for Automated Tools

When developing scripts or logic to interact with these maps, consider the following best practices:

### Case Sensitivity
ISO codes in SimpleMaps SVGs are almost exclusively uppercase. Always transform input codes to uppercase before attempting a selector match:
`const element = document.getElementById(isoCode.toUpperCase());`

### Fuzzy Name Matching
Users often provide names that don't match the SVG class names exactly. Use a fuzzy matching library or a simple normalization step (lowercase, remove punctuation) to compare names against the "SimpleMaps Name" column in the mismatch table.

### Handling Exclaves and Islands
For countries identified as "Multi-path" in Section 2, do not rely on `id`. Use the class selector:
`const paths = document.querySelectorAll('.Canada');`
This ensures that the Arctic islands are colored along with the mainland.

### Grouping and Aggregation
If a user asks to "color the European Union", the agent should maintain a mapping of EU member codes (AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK) and iterate through them.

### Data Validation
Before applying styles, verify the existence of the target element. SVG maps can vary slightly between versions:
```javascript
const target = document.getElementById(id);
if (target) {
  target.style.fill = color;
} else {
  const multiPaths = document.querySelectorAll('.' + className);
  multiPaths.forEach(p => p.style.fill = color);
}
```

### Disputed Regions Consistency
Be aware that certain regions like Western Sahara (EH) or Kosovo (XK) may be rendered as distinct paths or as part of a larger country depending on the specific map variant being used. Always perform an initial scan of the SVG to determine which identifiers are present.

## 8. Regional Hierarchy Reference

While SimpleMaps uses a flat structure in the SVG for individual paths, agents may need to group them.

*   **Scandinavia**: NO (Norway), SE (Sweden), DK (Denmark).
*   **Benelux**: BE (Belgium), NL (Netherlands), LU (Luxembourg).
*   **North America**: CA (Canada), US (United States), MX (Mexico).
*   **Australasia**: AU (Australia), NZ (New Zealand), and surrounding islands.
*   **Baltic States**: EE (Estonia), LV (Latvia), LT (Lithuania).

This reference ensures that high-level geographical requests can be translated into atomic SVG manipulations accurately and quickly.
