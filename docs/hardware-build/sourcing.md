# Sourcing parts

> Where to buy SeedSigner components and what to watch out for.

All SeedSigner components are standard, widely available electronics.

## Raspberry Pi Zero v1.3

The Pi Zero v1.3 is an older model and can be **hard to find in stock**. It is worth the effort if you want a hardware-guaranteed air gap, but expect to check a few shops before you find one.

Places to look:

- **Official Raspberry Pi distributors** — Check the [Raspberry Pi products page](https://www.raspberrypi.com/products/) for a list of approved resellers in your country.
- **Adafruit** (adafruit.com)
- **PiShop** (pishop.us)
- **Vilros**, **CanaKit**, and other Pi-focused retailers

If you cannot find a v1.3, any compatible Pi model will work. See the [components list](/hardware-build/components.md) for details on the software air gap available since v0.4.5.

## Waveshare 1.3" 240x240 LCD HAT

This display is reliably in stock from:

- **waveshare.com** (the manufacturer's own store)
- Major electronics distributors and marketplaces

> **Warning:** Waveshare makes many LCD HATs in different sizes and resolutions. Confirm the listing specifies **1.3 inch** and **240x240 pixels** before purchasing. A display with the wrong resolution will not work with SeedSigner.

## Camera module

OV5647-based camera modules are common and inexpensive. You can find them at:

- **Amazon**
- **AliExpress**
- **Adafruit, PiShop**, and other Pi retailers

If you are using a Pi Zero, make sure your order includes the **narrow Zero-compatible ribbon cable** (gold-colored connector). Some listings include both the standard and Zero cables; others only include the standard one.

If you already know which [enclosure](/hardware-build/enclosures.md) you plan to use, check whether it calls for the standard or compact camera board before ordering.

## A note on privacy

SeedSigner's components are **generic electronics** — a small computer, a display, and a camera. Nothing in your order signals "Bitcoin" to a merchant, payment processor, or shipping carrier. There is no branded packaging or product name that ties your purchase to cryptocurrency.

This is a deliberate design advantage. If you value purchasing privacy, SeedSigner's commodity hardware helps you maintain it.
