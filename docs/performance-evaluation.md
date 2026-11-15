\# Performance Evaluation Report



\## 1. Introduction



This performance evaluation measures the application-level response time of the Secure Code Review Framework's authentication and role-based access control (RBAC) application.



The objective is to evaluate how quickly the application's primary routes respond under sequential local testing.



\## 2. Testing Environment



| Parameter | Configuration |

|---|---|

| Operating System | Windows |

| Programming Language | Python 3.12.10 |

| Framework | Flask 3.1.3 |

| Database | SQLite |

| Testing Method | Flask Test Client |

| Requests per Route | 50 |

| Warm-up Requests per Route | 5 |

| Number of Routes | 5 |

| Total Measured Requests | 250 |



A temporary SQLite database was used to isolate the benchmark from the application's existing database.



Separate test clients were configured for unauthenticated users, normal users, and administrators.



\## 3. Performance Metrics



The following metrics were collected:



\- \*\*Average Response Time:\*\* Mean time taken to process a request.

\- \*\*Median Response Time:\*\* Middle value of the measured response times.

\- \*\*95th Percentile:\*\* Response time within which 95% of measured requests completed.

\- \*\*Maximum Response Time:\*\* Highest observed response time.

\- \*\*Sequential Requests per Second:\*\* Estimated request rate based on the reciprocal of average response time. This is not a concurrent load-test result.



\## 4. Performance Results



| Application Route | Average (ms) | Median (ms) | 95th Percentile (ms) | Maximum (ms) |

|---|---:|---:|---:|---:|

| Home Page | 0.538 | 0.506 | 0.634 | 1.027 |

| Login Page | 0.900 | 0.846 | 1.135 | 1.290 |

| Registration Page | 0.885 | 0.827 | 1.159 | 1.425 |

| User Dashboard | 1.492 | 1.427 | 1.893 | 2.108 |

| Admin Dashboard | 2.306 | 2.209 | 2.976 | 3.484 |



\### Overall Results



\- Routes evaluated: 5

\- Requests per route: 50

\- Total measured requests: 250

\- Overall average response time: 1.224 ms

\- All benchmark requests completed successfully.



\## 5. Performance Analysis



The home page demonstrated the lowest average response time at 0.538 ms.



The login and registration pages recorded average response times below 1 ms.



The user dashboard recorded an average response time of 1.492 ms because it retrieves user information from the SQLite database.



The administrator dashboard recorded the highest average response time at 2.306 ms. This is expected because the route performs database operations to verify administrator privileges and retrieve registered users.



The measured response times indicate that the tested application routes execute quickly in the local testing environment.



\## 6. Testing Limitations



This evaluation used Flask's in-process test client.



Therefore:



\- Network latency was not measured.

\- Concurrent-user performance was not evaluated.

\- Large-scale traffic handling was not tested.

\- Registration and login POST operations were not included in the benchmark.

\- Performance under production server conditions may differ.



The results should therefore be interpreted as local application-level response-time measurements rather than production load-testing results.



\## 7. Conclusion



The Secure Code Review Framework's authentication application successfully completed all 250 measured requests across five application routes.



The overall average response time was 1.224 ms.



The administrator dashboard recorded the highest average response time, while the home page recorded the lowest.



The evaluation establishes a baseline for the application's local response-time performance. Further testing using concurrent requests and a production-like deployment environment would provide a more comprehensive assessment of scalability and performance.

