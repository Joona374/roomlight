# Domain Model for RoomLight System

## 1. Roles

| Noun (/ Synonym) | Description | Relationships | Prototype Scope |
|------|------------|---------------|-----------------|
| Guest | A person staying in a hotel room using the lighting system. | Uses Control Panel, interacts with Room Lighting | ✔ |
| Revisiting Guest (Subtype of Guest) | A returning guest (hopefully) familiar with the standardized system. | Inherits Guest behavior | ✔ |
| Staff | Hotel employees managing rooms and lighting configurations. | Uses Dashboard, manages Templates, interacts with Rooms | ✔ |

---

## 2. Physical Structure

| Noun (/ Synonym) | Description | Relationships | Prototype Scope |
|------|------------|---------------|-----------------|
| Hotel Room | A single guest room with varying sizes and a lighting system installed. | Contains Lights and Panels, belongs to Floor | ✔ |
| Floor | A level within a property. | Contains Rooms | ✔ |
| Property | A hotel or building containing rooms. | Contains Floors | ✔ (simplified) |

---

## 3. Lighting System Components

| Noun (/ Synonym) | Description | Relationships | Prototype Scope |
|------|------------|---------------|-----------------|
| Wireless Light Module / Lights | Physical lighting units installed in rooms. | Controlled by Control Panel | ✔ (simulated) |
| Smart Wall Panels / Control Panel | Interface for controlling lights in a room. | Controls Lights, used by Guest | ✔ (virtual UI) |
| Lighting Template | Predefined lighting configuration for a room type. | Created by Staff, applied to Rooms | ✔ |
| Room Lighting State | Current state of lights in a room (on/off/dimmed/other). | Controlled via Panel or Dashboard | ✔ |

---

## 4. Digital System & Interfaces

| Noun (/ Synonym) | Description | Relationships | Prototype Scope |
|------|------------|---------------|-----------------|
| Dashboard / Centralized Interface | System used by staff to manage rooms and lighting. | Used by Staff, controls Rooms, applies Templates | ✔ |
| Energy Consumption View | Interface showing energy usage data. | Linked to Room (for Guests) and Dashboard (for Staff) | ✖ |
| Smartphone Control | Guest using own smartphone to control room. | Access via QR Code | ✖ |
| Room-specific QR Code | Unique identifier to connect smartphone to room. | Links Smartphone to Room | ✖ |

---

## 5. Other

| Noun (/ Synonym) | Description | Relationships | Prototype Scope |
|------|------------|---------------|-----------------|
| Existing Wiring Infrastructure | Pre-existing electrical wiring intended for lights in hotel rooms. | Supports Lights and Panels | ✖ |
| Pairing Process | Process of connecting physical devices (Controll panels and Lights) within a Room. | Links Lights an Panels in a Room | ✖ |
| Unauthorized Access | Security concern for system misuse. | Validation for Room-specific QR Code use | ✖ |
| Checkout Event | Trigger when a guest leaves room or hotel. | Initiates actions like turning off lights | ✔ |
| Pre-arrival Setup Event | Trigger before guest arrival to prepare room lighting. | Initiated via Dashboard | ✔ |

---

# Prototype Scope Summary

The prototype focuses on demonstrating:

- Staff creating and managing **Lighting Templates**
- Applying templates to **Rooms / Floors**
- Controlling **Room Lighting State** remotely via **Dashboard**
- Simulating **Guest interaction** via Control Panel
- Handling **Checkout** and **Pre-arrival** events

## Included Core Models
- Staff
- Guest (incl. Revisiting Guest)
- Property / Floor / Room
- Lighting Template
- Room Lighting State
- Control Panel (virtual)
- Lights (simulated)
- Dashboard
- Checkout Event
- Pre-arrival Setup Event

## Excluded (Out of Scope for Prototype)
- Energy Consumption View
- Smartphone / QR Code access
- Hardware constraints (wiring)
- Pairing process
- Security (unauthorized access handling)
