
# Requirements for a Localization Technology:
The customer has to navigate in a big indoor area and needs an accuracy of at most 1m so that it's clear in which aisle she currently is. We assume that most customers have a smart phone with them.


# GPS:
The most common localization technology is definitely not possible as there will be either no reception at all or the accuracy will be every poor. 


# Bluetooth:
The Localization with Bluetooth works similar to GPS with the difference that no satellites are use but a number of small bluetooth beacons that are distributed throughout the store. The smart device captures their signals and uses a prepared map of the store to find out where it is. 
If a store wants to offer the Product Navigator, a number of beacons have to be installed and connected to the power grid. No line of sight is needed so that they could be hidden in the suspended ceiling. After all devices are mounted, the map is created by walking around and manually marking positions. A guide on how to set up such a system can be found here (https://developer.here.com/products/indoor-positioning). 

The accuracy of such a system is good enough to localize a customer it however requires an investment into hardware and trained personel to create and update the map. 

# Ultra-wide-band, Wifi
There are other quite similar methods that also rely on multiple stationary radio emitters such as Wifi or UWB (Ultra-wide-band). The methods differ a bit in terms of cost and accuracy but all have the drawback of required additional hardware and labor. 


# Camera based:
All smart phones have cameras that can be used to compute the position of the phone relative to an object (marker) in the world. This marker has to be a) easy to detect in a camera so that the most common choice are QR-codes or similar shapes and b) its position in the world has to be known. It would therefore be possible to add new markers onto each shelf which would require manual labour and a process to print and distribute the markers. 
As we wanted to find a solution that is simple to integrate, we looked a bit closer and found that all price tags in the Rewe contain a 7-digit product id. We therefore decided to use Optical Character Recognition (OCR) to extract this id and use this information to localize the customer in the store. 

Setup in the store:
As the position of each product in the store is not exactly defined we first have to create a map. This requires a worker (e.g. someone who normally restocks the shelf) to walk by all shelves with a smartphone with one version of our app. The worker tells the app which layer of which aisle he wants to measure and the app automatically extracts the product ids and stores them in the backend. [Link to Video]. In this version of the App, the OCR is done on the device (no internet connection required) and can read the IDs from an image in around 100ms. 
This has to be done once for the whole store and each time the position of a product was changed. The process however is very fast and does not require a special training. 

User experience:
We implemented the user app as a website so that the user does not have to download and install an app when he wants to test the application. Only a QR-code at the entrance of the store is needed to tell the customers about the new Navigator. 

If the user wants to know her position in the store, she only has to quickly capture an image of a nearby price tag. The app extracts the product id and uses the previously generated map to look up the position of this product and with that, that position of the user. (In case a product can be found multiple times, the user has to capture an image of an additional product nearby).

We then use the compass to also send the customer in the right direction. In the final product, we would also use the gyroscope with a step detection to measure the walking speed to improve the localization accuracy. 



# Possible further use cases:
The exact position of products could be interesting for customers with impaired mobility (e.g. wheelchair users) that can't reach into the highest shelf to know if they need assistance to collect all items on their shopping list. 

We currently find the shortest route through a store, but the final app could offer multiple routes, e.g. by adding the current special offers to the route or by optimizing the route so that fragile products are picked up last (if the detour is not too large). 


 






 
