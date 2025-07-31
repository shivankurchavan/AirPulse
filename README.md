# AirPulse: Real-time Data Pipeline with Kafka, Prometheus, and Grafana

## Introduction

Welcome to AirPulse! This project demonstrates a real-time data pipeline for processing and monitoring data streams. It uses Apache Kafka as a high-throughput, distributed messaging system, a Python producer to send data into Kafka, Prometheus for collecting metrics, and Grafana for visualizing them.

This setup is the foundation for a scalable, observable, and robust data streaming architecture.

## Index

1.  [How to Set Up the Project](#how-to-set-up-the-project)
2.  [Technologies Used](#technologies-used)
3.  [Project Logic](#project-logic)
4.  [Future Scope](#future-scope)

---

## How to Set Up the Project

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Project

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>/newProj
    ```

2.  **Start all services:**
    Use Docker Compose to build the images and start all the containers.
    ```bash
    docker compose up --build
    ```
    This command will start the Kafka broker, Prometheus, Grafana, and the Python producer. The producer will start sending messages to the Kafka topic.

### Setting up Prometheus and Grafana

#### Prometheus

1.  Once the containers are running, you can access the Prometheus UI in your browser at:
    [http://localhost:9090](http://localhost:9090)

2.  To verify that Prometheus is scraping metrics from Kafka, go to **Status -> Targets**. You should see a `kafka` target with a state of `UP`.

#### Grafana Dashboard

1.  **Access Grafana:**
    Open your browser and go to [http://localhost:3000](http://localhost:3000).

2.  **Login:**
    Use the default credentials:
    *   **Username:** `admin`
    *   **Password:** `admin`
    You will be prompted to change your password on first login.

3.  **Add Prometheus as a Data Source:**
    *   On the left menu, go to **Connections -> Data Sources**.
    *   Click **"Add data source"** and select **Prometheus**.
    *   Set the **Prometheus server URL** to `http://prometheus:9090`.
    *   Click **"Save & test"**. You should see a confirmation that the data source is working.

4.  **Import a Grafana Dashboard for Kafka:**
    Grafana has a vast library of pre-built dashboards. A great one for monitoring Kafka with the JMX exporter is the "Kafka Exporter" dashboard.
    *   On the left menu, click the **"+"** icon and select **"Import dashboard"**.
    *   In the "Import via grafana.com" field, enter the dashboard ID `721` and click **"Load"**.
    *   On the next screen, select your Prometheus data source from the dropdown menu.
    *   Click **"Import"**.

You will now have a comprehensive dashboard for monitoring your Kafka broker's performance in real-time!

---

## Technologies Used

*   **Docker & Docker Compose:** For containerizing the application services and orchestrating them in a development environment.
*   **Apache Kafka:** A distributed event streaming platform used as the central message broker.
*   **Python:** Used for the data producer script that sends data to Kafka.
*   **JMX Exporter:** A Java agent that scrapes JMX MBeans from a JVM and exposes them as an HTTP endpoint for Prometheus to scrape.
*   **Prometheus:** An open-source monitoring and alerting toolkit used to collect time-series data from the Kafka broker.
*   **Grafana:** An open-source platform for monitoring and observability, used to create interactive dashboards to visualize the metrics collected by Prometheus.

---

## Project Logic

The data flows through the system as follows:

1.  **Producer:** The Python script in the `producer` service reads data (e.g., from a CSV file or a real-time API) and publishes it as messages to a topic in Apache Kafka.

2.  **Kafka Broker:** The `broker` service, running Apache Kafka, receives these messages and stores them durably in a topic. It is configured with the JMX Exporter java agent, which exposes Kafka's internal performance metrics (like message rates, latency, topic sizes, etc.) on port `7071`.

3.  **Prometheus:** The `prometheus` service is configured via its `prometheus.yml` file to scrape the metrics exposed by Kafka's JMX Exporter. It periodically polls the endpoint, stores the metrics in its time-series database, and makes them available for querying.

4.  **Grafana:** The `grafana` service provides a user interface for data visualization. It is connected to Prometheus as a data source. Users can build dashboards with panels that query Prometheus to display the Kafka metrics in a meaningful way, allowing for real-time monitoring of the entire pipeline's health and performance.

---

## Future Scope

This project provides a solid foundation that can be extended in many ways:

*   **Add a Stream Processor:** Introduce a stream processing framework like **Apache Spark** or **Apache Flink** to consume data from Kafka in real-time, perform complex transformations, aggregations, or analytics.
*   **Data Storage:** Store the processed data from the stream processor into a database, such as PostgreSQL for structured data, InfluxDB for time-series data, or a data lake.
*   **Advanced Dashboards and Alerting:** Create more sophisticated Grafana dashboards and set up alerting rules in Prometheus or Grafana to get notified of anomalies or performance degradation (e.g., high message latency, low throughput).
*   **Schema Registry:** Integrate a schema registry like the Confluent Schema Registry to enforce schemas for the data in Kafka, preventing data quality issues.
*   **Scalability:** Scale out the Kafka cluster to multiple brokers and the processing to a multi-node Spark/Flink cluster to handle higher volumes of data.
*   **End-to-End Testing:** Implement an integration testing suite to ensure the reliability of the entire pipeline.
