**UNIVERSITY WASTE MANAGEMENT SYSTEM**

## **1\. Introduction**

The increasing focus on sustainability and environmental responsibility has made efficient waste management a priority for many organizations, including educational institutions. At the University of Michigan–Flint, the Planet Blue initiative oversees waste management across campus buildings.

The Waste Management System (WMS) is designed to support these sustainability initiatives by helping the Planet Blue team effectively record, manage, and analyze campus waste data. The system provides a centralized database for tracking waste collection activities across university buildings, including details about waste types, bins, collection events, and staff responsibilities.

By organizing this information in a structured database, the system enables Planet Blue to generate analytical reports, monitor recycling and composting progress, and make data-driven decisions that reduce environmental impact and improve operational efficiency.

## **2\. Project Requirements (PR)**

This section outlines the requirements of the proposed Waste Management System (WMS):

| S/n | Requirement | Description |
| :---- | ----- | ----- |
| 1\. | Manage Building Information  | The system will store and manage information about university buildings, including building name, location, and associated department |
| 2\. | Manage Waste Types | The system will maintain a list of waste categories such as recyclable, compost, landfill, and hazardous waste.  |
| 3\. | Manage Collection Bins | The system will record details of waste bins placed in various buildings, including bin ID, capacity, location, and the type of waste they collect. |
| 4\. | Record Collection Events | The system will record data on waste collection activities (date, weight, waste type, staff, location). |
| 5\. | Manage Staff Records | The system will maintain information about staff members responsible for collection, including names, contact details, and assigned buildings. |

## **3\. ER Schema**

For this system, there are five main entity sets and their corresponding attributes. These entities represent the key components of the Waste Management System and record all essential data required for managing campus waste collection activities.

| ENTITY SET | ATTRIBUTES | DESCRIPTION |
| ----- | ----- | ----- |
| **BUILDING** | buildingPrefix, buildingName,buildingFloor | Stores campus buildings where waste is collected. |
| **STAFF** | staffID, staffName,currentShift | Stores data of staff responsible for waste collection and the shift worked. |
| **COLLECTION\_BIN** | binID, binLocation | Stores details of bins located in buildings. |
| **WASTE** | wastetypeID, typeName | Stores lookup data for the specific types of waste collected (e.g., Paper, Plastic). |
| **COLLECTION\_EVENT** | collectionID, collectionDate,collectionWeight, wasteTypeID, staffID | Stores the details of each actual waste collection event. |

## **4\. ER Diagram**

The ER diagram provides a visual representation of the main entities in the Waste Management System and how they are related. 

![][image1]

## **5\. Relationship Summary**

The section describes how the entities in the Waste Management System interact with each other. It defines the connections between buildings, bins, waste types, staff, and collection events.

| From Entity | Relationship Type | To Entity | Cardinality Interpretation |
| :---- | :---- | :---- | :---- |
| **Staff** | Exactly one | **Building** |  At every instance, each building has exactly one staff collecting waste |
| **collectionBin** | Many-to-One | **Building** | At each instance, a bin belongs to exactly one bin |
| **Staff** | One-to-Many (1:M) | **collectionEvent** | One staff can carry out many collection events |
| **collectionBin** | Exactly one | **Waste** | Collection Bin has exactly one waste(type) |

