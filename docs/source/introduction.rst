Introduction
============
Currently, there are a variety of mobile and smartwatch applications available that are designed to help patients take their medication correctly. These applications require patients to manually add dosage information and intake schedule for each medication, and provide automated reminders to take medication accordingly. In other words, the burden of correctly taking medication is placed entirely on the patient and there is no mechanism for verifying that a patient did indeed do so. We believe this to be a fundamental flaw and attempt to address it by integrating both patients and doctors into a single feedback loop in which:

1. Doctors upload patient medication information to an internal online portal.

2. This information is automatically propagated to a patient’s mobile device.

3. Patients receive automated alerts to take medication via mobile & smartwatch devices.

4. Correct medication intake is verified both by patient input and a ML model.

5. The doctors’ internal portal is updated with this information, allowing doctors to:

6. Take corrective action if a patient fails to take medication as prescribed.

7. Submit a prescription refill order to a patient’s pharmacy if needed.

Patients are alerted to pick-up medication refills at their local pharmacy or are notified that they have completed the course of treatment for the given medication.
Our goal is to implement this feedback loop via a multi-platform system composed of the following three components:

1. A quiet Apple Watch app that fades seamlessly into the background, notifying patients only when it is time to take their medication.

2. An accompanying iPhone app that displays a clean and minimal dashboard presenting a patient’s medication schedule for the current week.

3. An internal web app presenting doctors with a bird’s-eye-view of all of their patients.
