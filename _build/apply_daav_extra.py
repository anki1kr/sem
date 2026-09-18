"""DAAV: NoSQL advantages/disadvantages, case study + real-world DS sections, Q&A, and an
'Important questions' index at the top of each unit. Backs up first."""
import shutil
from pathlib import Path

F = Path("frag")
Path("backup").mkdir(exist_ok=True)
for n in ("daav-u1.html", "daav-u2.html"):
    shutil.copy(F / n, Path("backup") / n)


def swap(s, old, new):
    assert s.count(old) == 1, (old[:60], s.count(old))
    return s.replace(old, new)


u1 = (F / "daav-u1.html").read_text(encoding="utf-8")
nosql = """<h4>Advantages and disadvantages of NoSQL</h4>
<div class="tw"><table><tr><th>Advantages</th><th>Disadvantages</th></tr>
<tr><td><mark>Horizontal scaling</mark> on cheap commodity servers</td><td><mark>Weaker consistency</mark>: many systems are eventually consistent (BASE), not strictly ACID</td></tr>
<tr><td><mark>Flexible schema</mark>: add fields without ALTER TABLE</td><td><mark>No standard query language</mark>: each product has its own API</td></tr>
<tr><td>Handles <mark>structured, semi-structured and unstructured</mark> data</td><td><mark>Joins and complex queries</mark> are weak or missing</td></tr>
<tr><td><mark>High availability</mark> through replication</td><td><mark>Data duplication</mark> (denormalisation) wastes space and must be kept in sync</td></tr>
<tr><td><mark>Fast reads and writes</mark> for simple access patterns</td><td>Less mature tooling, reporting and skilled people than SQL</td></tr>
<tr><td>Mostly <mark>open source</mark>, lower cost</td><td>Not suited to multi-row transactions such as banking ledgers</td></tr>
<tr><td>Data stored close to application objects (fewer mappings)</td><td>Schema flexibility can let inconsistent data creep in</td></tr></table></div>
<p><b>When to use NoSQL:</b> huge, fast-growing, varied data with simple access patterns (product catalogues, user sessions, social feeds, IoT readings). <b>When to stay with RDBMS:</b> strong consistency and complex joins (banking, accounting, inventory).</p>
<h4>CAP theorem (Brewer)</h4>"""
u1 = swap(u1, "<h4>CAP theorem (Brewer)</h4>", nosql)

index1 = """<section class="topic" id="u1-important">
<h3>Important questions (Unit I)</h3>
<ol>
<li>What is Big Data? Discuss in detail → <a href="#u1-intro">1.1</a>, <a href="#u1-char">1.2</a></li>
<li>Sources of Big Data → <a href="#u1-sources">1.4</a></li>
<li>Types of Big Data with real-world examples → <a href="#u1-types">1.3</a></li>
<li>Technologies used in Big Data (Hadoop, HDFS, NoSQL, open source) → <a href="#u1-tech">1.6</a>, <a href="#u1-hadoop">1.8</a>, <a href="#u1-hdfs">1.9</a>, <a href="#u1-nosql">1.13</a>, <a href="#u1-ecosystem">1.12</a></li>
<li>Hadoop architecture and how it helps Big Data → <a href="#u1-yarn">1.11</a>, <a href="#u1-hadoop">1.8</a></li>
<li>5 V's of Big Data → <a href="#u1-char">1.2</a></li>
<li>NoSQL: why use it, advantages and disadvantages → <a href="#u1-nosql">1.13</a>, <a href="#u1-nosqltypes">1.14</a></li>
<li>Integrating diverse data; aggregate data model → <a href="#u1-integ">1.7</a>, <a href="#u1-aggregate">1.15</a></li>
</ol>
</section>
"""
u1 = swap(u1, '<section class="topic" id="u1-intro">', index1 + '<section class="topic" id="u1-intro">')
u1 = swap(u1, "</dl>", """<dt>Give two advantages and two disadvantages of NoSQL.</dt><dd>Advantages: horizontal scaling on commodity servers; flexible schema for semi-structured data. Disadvantages: weaker (eventual) consistency; no standard query language and weak joins.</dd>
</dl>""")
(F / "daav-u1.html").write_text(u1, encoding="utf-8")

u2 = (F / "daav-u2.html").read_text(encoding="utf-8")
extra = Path("daav_extra.html").read_text(encoding="utf-8")
u2 = swap(u2, '<section class="topic" id="u2-short">', extra + '<section class="topic" id="u2-short">')
u2 = swap(u2, "<h3>2.13 Short answers (1.5 marks)</h3>", "<h3>2.15 Short answers (1.5 marks)</h3>")
u2 = swap(u2, "<h3>2.14 Long-answer frames (15 marks)</h3>", "<h3>2.16 Long-answer frames (15 marks)</h3>")
index2 = """<section class="topic" id="u2-important">
<h3>Important questions (Unit II)</h3>
<ol>
<li>What is Data Science? Its components and the 5 P's → <a href="#u2-value">2.1</a>, <a href="#u2-components">2.3</a>, <a href="#u2-5p">2.4</a></li>
<li>Complete data science process with an example → <a href="#u2-process">2.5</a></li>
<li>Big data modeling and management: ingestion, storage, security, scalability → <a href="#u2-mgmt">2.6</a>, <a href="#u2-ingestion">2.7</a>, <a href="#u2-storage">2.8</a>, <a href="#u2-scale-sec">2.11</a></li>
<li>Case study: Big Data Management Plan for customer data → <a href="#u2-case">2.13</a></li>
<li>Real-world data science example and advanced techniques → <a href="#u2-realworld">2.14</a></li>
</ol>
</section>
"""
first2 = '<section class="topic" id="u2-value">'
u2 = swap(u2, first2, index2 + first2)
u2 = swap(u2, "</dl>", """<dt>What is a big data management plan?</dt><dd>A design stating how data is ingested, stored, kept at good quality, processed (operations), scaled and secured for an organisation's data.</dd>
<dt>Why is a data lake used for customer data from web, app and social media?</dt><dd>It stores raw data of every type (structured, JSON, text, images) cheaply at scale, with schema applied only when data is read.</dd>
<dt>What is collaborative filtering?</dt><dd>A recommendation technique that suggests items liked by users with similar behaviour, measured with a similarity such as cosine similarity.</dd>
<dt>What is A/B testing?</dt><dd>Showing two versions to two random groups of users and keeping the version that performs better on a chosen metric.</dd>
</dl>""")
tail = '<a class="top" href="#top">↑ top</a>\n</section>\n</section>'
assert u2.rstrip().endswith(tail)
u2 = u2.rstrip()[: -len(tail)] + """<h4>Q8. A company collects customer information from websites, applications and social media. Design a Big Data Management Plan.</h4>
<ol>
<li>State assumptions: sources, data types, about 5 million events/day at 2 KB (10 GB/day, about 11 TB/year with replication 3).</li>
<li>Draw Fig 2.15 (sources → ingestion → storage → quality → operations → reports, wrapped by scalability and security).</li>
<li>Ingestion: streaming for clicks and app events, batch for orders and social exports, buffer with a message queue.</li>
<li>Storage: data lake for raw data, NoSQL for profiles and events, warehouse for reports.</li>
<li>Data quality: dedupe across channels, validate, standardise, missing values, outliers, entity resolution.</li>
<li>Operations: filter, join, aggregate, top-N, sentiment analysis, 360° customer view.</li>
<li>Scalability: scale out, partitioning, replication, auto-scaling on sale days.</li>
<li>Security: encryption, Kerberos + role-based access, masking, audit, consent and retention (DPDP Act, 2023). Conclude with the business outcome.</li>
</ol>
<h4>Q9. Describe a real-world example where data science is used and explain the advanced techniques involved.</h4>
<ol>
<li>Pick recommendation systems (streaming service); define them.</li>
<li>Walk through the 5 steps, draw Fig 2.16.</li>
<li>Netflix Prize fact (2006–2009, US$1 million, matrix factorisation).</li>
<li>Techniques table: collaborative filtering, matrix factorisation, content-based, deep learning, NLP, computer vision, clustering, forecasting, A/B testing, Spark.</li>
<li>Numerical: cosine similarity sim(A, B) = 0.979, sim(A, C) = 0.261 ⇒ recommend from B.</li>
<li>Other uses: fraud detection, delivery-time prediction, crop disease detection; conclusion.</li>
</ol>
""" + tail + "\n"
(F / "daav-u2.html").write_text(u2, encoding="utf-8")
print("ok")
