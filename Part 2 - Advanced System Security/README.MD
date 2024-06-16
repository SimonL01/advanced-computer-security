# Synthesis
**INFO8013 - Advanced Computer Security**

*Teaching Staff* : 
Benoît Donnet
Laurent Mathy

*Teaching Assisstant* :
Vincent Jacquot

# Table  of Contents

1. [Part 2 : Advanced Cryptography](#part-2-advanced-cryptography)
    1. [Chapter 1 : Trusted Computing](#trusted-computing)
        1. [Secure Remote Computing and Trusted Computing]
        2. [Trusted Computing Implementation Principles]
        3. [Trusted Computing Attacks]
    2. [Chapter 2 : Side-Channel Attacks](#side-channel-attacks)
    3. [Chapter 3 : Fuzzing](#fuzzing)

## Part 2 Advanced Cryptography

### Trusted Computing

#### Secure Remote Computing and Trusted Computing

##### The problem

* What is the Problem Regarding Secure Remote Computing ?
    - Executing software on remote computer owned, maintained and operated by an untrusted party
    - We want to do this with some integrity and confidentiality guarantees
    - You could assume that only part of the software that you want to run needs those integrity and confidentiality guarantees and also part of the data
    - Actually, part of the process you want to run can be run in the untrusted environment without any special checks and only one part needs to be executed with the integrity and confidentiality guarantees
    - To make it clearer, tt's not necessarily done like that but we could imagine that the part where we need the guarantee is actually a thread, doesn't have to be but it would simplify the intuition and understanding, and other threads that can run unchecked in the untrusted environment
    - Part of the data that those threads manpulate will have to have those integrity and confidentiality guarantees

* The Problem

![Local Image](/images/trusted/T1.PNG)

The data owner who wants to run some program and of course if you run a program, you should only run it if you trust it (which is why OpenSource is better than Closed Source because you can trust that a lot of eyeballs have had a look at it and tried to find issues with it).
That person wants to run its program on its data on somebody else's computer. The problem is that the data owner doesn't necessarilly trust the infrastructure owner (person who owns the computer where you run the computations).
The idea is that the part of the program and the data that need to have integrity and confidentiality guarantees will have to run somehow in some form of container on remote computer (need some setup configurations, send code, send the data, establish some secure communication channels between the data owners computers and containers so that you can send data securily to its container, whatever the code inside the container will do its thing on the private data and result will have to be sent back in an encrypted form to data owner computer so infrastructure owner cannot peek inside the data and see rssults produced by the container).
Everything outside the container is untrusted.
Here, when we talk about a container, it is a word, we are not invoking necessarily containers like virtual machines.
Here what we mean is just a place in computer where protected computations will run and part of the container is also all the mechanisms that need to be put in place to make the computations protected.

##### Context

* Why would I want to do this ? 
    - Cloud computing is a prime example of a place, an infrastructure where you might actually not completely trust the infrastructure owner and where it is sometimes problematic from a privacy perspective for instance to go and do computations
    - Obviously, Cloud computing is very convenient (computing capacity is very easily scalable up and down)
    - As far as you are concerned, the infrastructure is pretty much virtual, you can add and remove compute resources and storage resources very easily (big advantage)
    - Run a lot of computations without yourself owning much infrastructure
    - For example the webex meeting with the teacher is going through the webex cloud (university had not forseen the problem of confinent but it was easy to scale because it was not the university's infrastructure and we could get a piece of that easily to scale)
    - Very confidential data, ask yourself can you really trust the infrastructure provider to repsect privacy and not try and gain insights of the data they are not supposed to
    - Confidential data (medical image analysis, banking, mobile phone contact analysis, ...)
    - Imagine you have an algorithm to recognize some medical image, you might want to go the cloud but of course you don't really want to send medical images to the clear to the cloud, these things are private to people
    - Bank might not want to deploy its own infrastructure but you don't want somebody to go and modify your data in the cloud etc breaking the integrity (of course confidentiality is very important too)
    - Might want to do contact analysis on the cloud because mobile operator might not have the infrastructure to do so
    - These days a lot of cloud computing is free but as they say, "if it's free, you are actually the product"

So, let's go back to the medical image analysis. What you might want to do is having a container with the analysis algorithm loaded into it. You might want to establish that container in a secure way and once the container is establish, you might want to have a secure channel between container and data owner. What will happen is that the data owner would upload the encrypted medical images through the cloud infrastructure. The upload can be done in an untrusted part of the infrastructure because the image is encrypted and all data is encrypted and somehow this data must make its way inside the container which decrypts the data, analyses it, encrypts the results and sends results back possibly staging the encrypted results out of the container before it is sent back to the data owner. Not all of the application code need to be inside the container but the critical part. This is possible with the encryption.

##### Holy Grail Solution

* Homomorphic encryption
    - form of encryption allowing computation on encrypted data (ciphertext) that produces an encrypted result that matches computation on plaintext when result is decrypted
    - idea : manipulate encrypted data without having to decrypt it
    - because you do not need to decrypt, the result produced are themselves encrypted
    - you can send data encrypted to infrastructure and do stuff on these data then produce encrypted results and results sent back to data owner which he, only, would decrypt
    - that would be the homomorphic encryption that creates the "container" we were talking about
    - the first problem is that there are homomorphic techniques and types of computations that can be solved with homomorphic encryption but the family of computations that can be solved with homomorphic computations is actually quite limited (no general purpose on homomorphic algorithms yet)
    - the second problem is that a impractical performance overhead incur (extremely resource intensive and in most cases, basically unusable of poor performance you get out of it)

* We are going to find something else. This something else is trusted computing

* Trust hardware manufacturer

![Local Image](/images/trusted/T2.PNG)

The change is that we are gonna be in the trust the hardware manufacturer.
The data owner and software provider still. The infrastructure owner still is not trusted but the data owner also trust the hardware manufacturer and hardware manufacturer builds the CPU.
To trust the hardware manufacturer means that we trust that this guy builds CPUs that work as advertise and what is advertise is that we have support for trusted computing.
Now we have trusted hardware platform that can run untrusted software (software used by infrastructure owner) but thanks to the trusted hardware, we can build secure containers where because of the way the hardware is built, we know or at least we can hope, that we can have secure computation.
Essentially, the difference between secure remote computing and trusted computing is that in SRC, we trust absolutely no one in the infrastructure, but in the TC, you actually trust the hardware manufacturer. Kind of an ally in the infrastructure that "simplifies" the problem.

Actually, we are going to limit our trust to only the CPU.
The CPU is gonna be the only piece of hardware that we trust in the infrastructure, everything else in the infrastructure on the remote system is untrusted.

We are in the worse case scenario because the owner of the infrastructure has access to the infrastructure.

The adversary has physical access to the machines. You must remember from introduction to computer security that an attacker that has access to physical system is all mighty because he can do stuff that a remote attacker cannot do such as for instance instrument physical buses on the machine, instruments components on the machine or even try and do some kind of reverse engineering on the components of the infrastructure and so on.
We don't trust the owner still because he could instrument.

I/O devices aren't truted on the remote system either because a lot of them have a debug mode which should have been switched off when they get deployed but most manufacturer keep that debug mode on simply to facilitate updates and feed debugging of their devices. So you can actually remotely reprogram those devices and change their code and again the infrastructure provider is actually not remote at home compared to devices that have direct access to them.

No going to trust also all the software on the remote machine, even kernel and/or VM hyperviser (VMM, virtual machine manager). Not even trusting the operating system because it is run by the infrastructure provider and do not trust him. He could have deployed a rogue kernel that could essentially remove a lot of protection we try to put in for our trusted computing environment. 

We also saw that even if you trust the kernel there are attacks, side-channel attacks that can actually expose pretty much all of the data in the remote environment. Those attacks remove protections that might have been put in and therefore even if you trust the kernel, you might not be able to trust the confidentiality you are trying to impose.

Pretty much everything is done because absolutely nothing is trusted on the remote system except for the CPU.

#### Trusted Computing Implementation Principles

* CPU reserves memory
    - Processor Reserved Memory (PRM)
    - That chunk of memory reserved by the CPU is called the PRM

* Secure containers (enclaves) by CPU in which we are going to run our trusted computation will be created in the PRM
    - All our enclaves will lived in our PRM
    - CPU protects PRM from all non-enclave memory access in order for all this to be useful
    - Everything outside an enclave cannot access the PRM and therefore as enclaves are inside PRM, anything outside enclave shouldn't be able to access enclave memory
    - Because you do not trust the Hypervisor/kernel, those guys will not be in PRM
    - This reminds of something : what we did to protect the kernel when we were trusting the kernel, we were putting the kernel into priviledge memory and everything that was not in priviledge memory could not access that priviledge memory and here it is kind of the same thing. We are creating the PRM and anything not in PRM cannot access PRM memory. PRM is kind of the same thing as priviledged memory but this is a different part of memory.

* Enclave Page Cache (EPC)
    - PRM is actually a part of DRAM
    - most trusted computing systems actually reserve a continuous block of memory simplifying a little bit the design
    - think of the PRM as a continuous block inside the DRAM that is protected from external access
    - inside the PRM we have an enclave page cache (EPC)
    - EPC is just a pool of pages that will be allocated to enclaves inside the PRM
    - We have metadata associated with those pages that hold all sorts of information about the pages and which enclave they have been allocated to and so on and so forth
    - That metadata is of course inside the PRM
    - The metadata is the EPCM which is also of course used for security checks
    - EPC is essentially a set of pages in PRM to be used by the enclaves
    
    ![Local Image](/images/trusted/T3.PNG)

    - How big is the PRM in general ? It depends on how many enclaves you want to support. You can configure how many enclaves you want to support (this is configurable) but if you are a cloud provider that is making a business out of providing trusted computing platform that could run into the multi gigabits but if the use of enclaves is fairly rare, then it could a few Kbits to Mbits. Configurable by the CPU. Priviledge memory was also configurable as a reminders

Remember that L1 cache is typically 32 Kb to 64 KB per core. L2 cache is typically 256 KB to 1 MB per core and L3 cache is typically 2 MB to 64 MB shared among cores in a CPU.

Caches are small, fast memory locations within the CPU that stores copies of frequently accessed data from main memory. They are essential for improving the performance and efficiency of the CPU by reducing the time it takes to access data.

* EPC is managed by system software
    - That is, it is managed by the kernel and/or the Hypervisor
    - The system software is the one that assigns EPC pages to enclaves
    - For page management, it is kind of the same for normal pages, it s actually the Operating System that decides which page is assigned to which enclave but you have additional security mechanism implemented by the CPU for instance, the CPU will use the metadata associated with each page to ensure for instance that each EPC page is never assigned to two enclaves simultaneously
    - The system software (either kernel and/or Hypervisor because as in the cloud, can assume everything is virtualized) will decide when and which EPC page gets swapped out or swapped in into the main memory and even into the PRM because you might want to support PRM "processes" virtual address spaces which are bigger than what can fit inside the PRM. There is no reason why you cannot do proper virtual memory management to support the scenario where the virtual memory is bigger than physical memory and which pages get swapped in or swapped out is decided by the system software.
    - CPU is obviously gonna have to help you because if the system software could just decide ok swap this page out and nothing else happen to the page so that the page gets swapped out normally, then you would just expose the content of that page to the rest of the system and since you are not trusting the rest of the system you absolutely do not want to do this
    - CPU needs to implement a specific page swap algorithm for EPC pages. This swapping mechanism consists in the CPU encrypting the EPC page before it is swapped out and also decrypting EPC pages that are swapped in back into PRM. To avoid replay attacks by a rogue kernel for instance, the CPU also uses nonces to ensure freshness of the pages that gets swapped back in into the PRM.
    - EPC pages are used to create isolated and secure regions of memory called enclaves within the main memory (Processor Reserved Memory). When the system needs to swap these pages out of PRM and into regular memory or disk storage, the pages need to be encrypted to maintain their confidentiality and integrity. When these pages are swapped back into the PRM, the CPU must ensure that they are the same pages that were originally swapped out, which is where encryption and nonces come into play.
    - In a replay attack, an adversary could capture and re-use old, legitimate data (such as previously swapped out pages) to interfere with the operation of the system. By replaying an old page, the attacker could revert the enclave to a previous state, potentially leaking sensitive information or causing the system to behave incorrectly.
    - A Nonce (number used once) is a unique value used to ensure that each encryption operation is unique. When the CPU encrypts a page before swapping it out, it includes a nonce in the encryption process. When the page is swapped back in, the CPU checks the nonce to ensure that the page is fresh and not a replay of an old page. CPU compares the nonce used during encryption and the one used during decryption, if they match, then page is fresh.
    - Nonce-based freshness checks provide a mechanism to verify the authenticity and freshness of swapped pages independently of the kernel that could be a rogue kernel
    - Because we need that encryption, decryption, obviously, it s going to take some time. So what the page management for the EPC pages says is that actually EPC pages are always swapped from PRM to DRAM first and then from DRAM to PRM. Only when the pages, the encrypted EPC pages have been swapped out of the PRM and are there for another part of the DRAM, then the system software can use it s normal page swapping algorithm to essentially decide or not to swap the evicted EPC pages out of DRAM onto disk.
    - We have a staging of the evicted EPC pages through DRAM as opposed to going straight on disk.

* Why is there a staging of the evicted EPC pages swapped from PRM out to DRAM first ?

Staging the evicted EPC pages swapped from PRM to DRAM first, rather then directly to disk serves several important purposes related to performance, efficiency and security.
- Speed of Access (DRAM faster than disk whether HDD or SSD) and reduced latency
- Minimizing disk I/O as DRAM acts as an intermediate storage that can hld pages temporaly until it is certain that they need to be written to disk, thus reducing unnecessary disk writes
- Integrity verification and encryption: encryption when page evicted from PRM to DRAM ensuring that any subsequent movement to disk does not expose plaintext data and by staging in DRAM, the system can perform necessary integrity checks before deciding to store them on disk ensuring only verified pages are written to slower storage
- DRAM is used as a staging area allowing the CPU to manage and verify nonces (used to ensure page freshness) more efficiently before pages are moved to a more permanent storage. This helps protect against replay attacks by ensuring pages have valid nonces before they are stored or retrieved
- Leveraging the strengths of each types of memory
- While PRM is part of DRAM, it is logically separated from the general DRAM ppol. This means that when EPC pages are evicted from PRM, they are moved to the general DRAM space before considered for disk storage.
- Evicted pages are kept in the general DRAM space, allowing faster access compared to if they wer directly written to disk. This minimizes the latency involved in bringing these pages back into the PRM when needed.
- Kind if buffering in DRAM

* Why can't EPC pages go straight to disk ?
    - Staging through unprotected DRAM ? Why ?
    - Because it's encrypted ? No the encryption is just there to protect the content. Once it is in unprotected DRAM, it is still encrypted and the system software will be able to throw it back onto the disk. The fact that it is encrypted isn't the problem.
    - Who in the system can access the disk ? The Operating system that has direct access and direct management of I/O devices. The OS accesses the disk and if you are in the virtual environment, then obviously, the hypervisor also is in that loop. That is why to access anything or put anything on the disk usually, user programs have to resort to system calls. But to evict an EPC page straight onto the disk, for this to happen, the OS would need to have direct access to that EPC page meaning the system software would have access, at least read access to the PRM. But since we are not trusting the system software, that access would violate the protection you need on the PRM. So you cannot let the operating system access the PRM and therefore, the CPU must first stage those EPC pages out of PRM and into untrusted DRAM where they can then be accessed by the untrusted system software.
    - The CPU takes this opportunity to also encrypt the page as it is evicting it from the PRM.

* Initializing the Enclave
    - We need to somehow initialize the enclave with the secure code that needs to run securely inside the enclave and potentially some original data that the enclave needs to be able to do its work (some kind of IP address of the data owner maybe, so that enclave can go back and establish a connection with data owner and be able to retrieve data).
    - Initial code and data for the enclave will be loaded by the system software. The system software loads up that code and the corresponding data for the enclave in untrusted pages in untrusted rams. Then asks the CPU to copy those pages from unprotected to EPC pages. CPUs have specific trusted computing instructions to support all those operations.
    - You basically send code for the enclave and associated data needed for initialization of the enclave to the untrusted system software and this guy plays the game or not, loads that up into untrusted pages and asks the CPU, please copy those pages into some EPC pages. Then, system software assigns the EPC pages to the enclave with instructions on the CPU to assign EPC pages to the enclaves and also the physical addresses of the corresponding EPC pages are inserted in the page table of the process containing the secure computation.
    - Initial enclave state known to potentially rogue system software because it has seen everything you put inside the enclave to initialize it.
    - After all enclave pages are loaded, the system software asks the CPU to mark that enclave as initialized.
    - Once initialized, loading, changing its initial state is prohibited by the CPU. Once system software has invoke initialize instruction for an enclave on the CPU, the CPU will essentially start refusing any modification to that enclave with a little exception we will talk about later.
    - In a sense, now, we have a copy of the initial enclave state inside the enclave itself.
    - Once initialized, the enclave could actually run the code inside it. But obviously, the initial state of the enclave is controlled by the system software since it is the one who prepared the copy for the CPU to the enclave. So we need to find a way for the remote client, the data owner to get assurances that the loaded code and its associated initial data is actually the trusted intended code that it wanted to send because the system software could change the code that was sent to it by the remote client and load its own untrusted rogue code into the enclave which would completely defeat the whole strategy.

* Making sure that the loaded code is the intended one is gonna be done through software attestation.
    - That software attestation is computed by the CPU and it s sent back to the verifier (the remote client) by the CPU itself
    - The software attestation architecture will be shown and explained in the next section.

##### Software Attestation

![Local Image](/images/trusted/T4.PNG)

We are going to go through how and why it works.

![Local Image](/images/trusted/T5.PNG)

First big component of the software attestation mechanism is the hardware manufacturer that you need to trust this guy and essentially, what the hardware manufacturer does in trusted computing is operate as a certification authority. So you have seen certificate and certification chains in computer security course. So essentially, what this means is the hardware manufacturer will generate a pair of asymmetric keys. Keep its private key private and have a public key (trusted public key) and this pair of keys will essentially make up the route key of the whole trust chain in the system. Obviously, this is a classical trust chain as we have them deployed these days with all certificates. That chain is only as secure as the private root key of the manufacturer. We need to trust that, the manufacturer root key, because if we don't, we are not trusting the trust chain and no trust at all is possible. The manufacturer is the intel, sort of.

Inside the CPU, the CPU will have a private key which should be held in tamper-resistant hardware. The public attestation key is also put inside the CPU but here it, it is possible to imagine that the certificate containing this public attestation key could be outside the CPU inside some kind of public key distribution infrastructure. Simplified, we can imagine that this public key certificate for the attestation key is inside the CPU.

Because the manufacturer is a certificate authority. What the manufacturer would do is actually sign with its private root key the endorsement certificate containing the CPU public attestation key.

For the moment, it is a classic certification chain applied to a pair of public/private keys that are CPU dependent.

This is where we see that for the whole thing to hold the hardware manufacturer must be trusted.

![Local Image](/images/trusted/T6.PNG)

We talked about that pair of attestation key. Those keys, especially the private key used by the CPU must be burned during manufacturing. So when the CPU leaves, that private key must be inside it and the correpsonding endorsement certificate (containing the public key corresponding to that private key) too. Instead the manufacturer could have put the public key inside a public key infrastructure owned by the manufacturer.

When we say that the private key is in the tamper-resistant hardware, the idea is that it should be unrecoverable by anything except by the CPU itself. How much you can build those tamper-resistant hardware to resist reverse engineering and so on and so forth is another question.

![Local Image](/images/trusted/T7.PNG)

Remember that the untrusted system software asks the CPU to copy the untrusted pages that contained the initial state of the enclave into the enclav. So, while doing this, the CPU actually can hash the content of those pages. The CPU, while it is building the enclave essentially computes a secure hash of the content of the enclave. So, CPU has computed what we called the "Measurement", essentially a hash of the enclave image which was computed at load time.

If privateAK leak, can't change it or you would have to change the hardware. That is a problem because if the private key is gone, then you better have a way to essentially revoke the endorsement certificate associated.

If somebody manages to recover that private key from the tamper-resistant hardware, that means they have probably reversed engineer the CPU so, if they have reversed engineer the private key, they probably are going to be able to recover the endorsement certificate. So you better be able to revoke that endorsement certificate.

Keys and certificates shown in the diagram play crucial roles in establishing trust and verifying the integrity and authenticity of the software and the hardware platform.

* Public Root Key (PubRK) and Private Root Key (PrivRK)
    - PubRK : this is the public key part of the Manufacturer Root Key pair. It is widely distributed and used by berifiers to validate signatures made by the corresponding private key. It is used to verify the endorsement certificate.
    - PrivRK : This is the private key part of the Manufacturer Root Key pair. It is kept secure and used by the Manufacturer Certificate Authority to sign endorsement certificates. The security of this key is paramount as it underpins the trust model for all devices issues by the manufacturer.
* Public Attestation Key (PubAK) and Private Attestation Key (PrivAK)
    - PubAK : This key is part of the attestation key pair used for attestation. It is contained within the Endorsement Certificate, which is signed by the Manufacturer Certificate Authority. The verifiers use this key to validate the attestation signature provided by the platform (hardware).
    - PrivAK : This key is securely stored within the tamper-resistant hardware of the platform. It is used to create the attestation signature. The integrity and confidentiality of this key are crucial to ensuring that only legitimate attestations are made.
* Endorsment certificate
    - This certificate contains the PubAK and is signed by the Manufacturer Certificate Authority using the PrivRK. It binds the PubAK to the hardware, indicating that the key is authentic and issued by a trusted manufacturer. Verifiers use the Manufacturer's PubRK to verify the signature on the endorsement certificate, establishing trust in the PubAK
* Tamper-Resistant Hardware
    - This hardware component securely stores the PrivAK. It ensures that the PriAK cannot be extracted or misused, maintaining the integrity of the attestation process. It is responsible for generating the attestation signature using the PrivAK
* Attestation Process
    - Key Generation and Certification : The tamper-resistant hardware generates the PubAK and PrivAK pair. The PubAK is sent to the Manufacturer Certificate Authority, which signs it with the PrivRK, creating the endorsement certificate.
    - Attestation signature : When attesting, the platform uses the PrivAK to sign a measurement of the software and potentially other relevant data. This signature (Attestation Signature) can be verified by a verifier using the PubAK contained in the endorsement certificate.
    - Verification : the verifier uses the Manufacturer's PubRK to verify the endorsement certificate. Then it uses the PubAK from the endorsement certificate to verify the attestation signature. If both verifications succeed, the verifier can trust the measurement and other data provided in the attestation, ensuring the integrity and authenticity of the platform.

* Verifier Role
    - The verifier receives the attestation report, which includes the data, the attestation signature and the endorsement certificate
    - Verification of the endorsement certificate : the endorsement certificate contains the PubAK and is signed by the Manufacturer Certificate Authority using the PriivRK. The verifier uses the Manufacturer's PubRK to verify the signature on the Endorsement Certificate. This step ensures that the PubAK is indeed issued by a trusted maufacturer and is valid.
    - Verification of the Attestation Signature : The verifier extract the PubAK from the endorsement certificate. The verifier uses the PubAK to verify the attestation signature on the data included in the attestation report. This involves decrypting the signature with the pubAK and comparing it to a hash of the received data to ensure they match.

So, the CPU has computed a hash of the enclave image and it will add that hash into the attestation and obviously, it will sign attestation with its private key and send this signed attestation to the verifier.

You should be able to convince yourself that this is enough as long as the private key is safe, to ensure that the untrusted software system has not changed the code and associated data to be loaded into the enclave. If the untrusted system software had tampered with the code or the initialization data, then the content of the enclave would be different than what was intended by the remote client and then that measurement sent back to the remote client would not be what is expected by the client and therefore, client would reject the attestation and abandon the secure enclave on the remote system.

![Local Image](/images/trusted/T8.PNG)

The remote client needs a secure channel with the enclave because the secure data or confidential data is not there yet. So you need a secure channel for the remote client to send the confidential data to the enclave so that secure computation can be run on it. Part of the attestation is also the data and that data is essentially a hash of a key exchange protocoll that happens between the verifier (the remote client) and the enclave. To exchange the encryption key for the secure channel between the enclave and the remote client, you use the classic Diffie-Hellman key exchange.

Diffie-Hellman : each side  send publicly a message containing a publicly visible piece of data and by each combining those pieces of data tohether, they establish a secret key between themselves and anybody in the middle who might have seen the exchange of messages and the two pieces of data in the clear cannot deduce the key. Formally, both parties agree on public parameters which are a  large prime number p and a primitive root g modulo p which aren't secret. Each party selects a private key such as $X_{1} = g^{x_{1}} \; mod \; p$ and $X_{2} = g^{x_{2}} \; mod \; p$. They exchange the public keys $X_{1}$ and $X_{2}$ over the public channel. And they compute the shared secret using the other public key : $s = X_{2}^{x_{1}} \; mod \; p$ and $s = X_{1}^{x_{2}} \; mod \; p$. The security relies on the difficulty of the Discrete Logarithm Problem : given g, p, and $A = g^{a} \; mod \; p$, it os computationally infeasible to determine a.

Those key exchange messages are hashed together and are added to the attestation.

![Local Image](/images/trusted/T9.PNG)

This attestation is signed by the CPU and is sent back to the remote client who can verify the signature and decide if the remote system has tampered with any of the code, the initial data and or the key exchange that happened between itself and the enclave.

The root public key, the endorsement certificate for the CPU and the attestation signature should ensure that the correct software was loaded on the trusted system. Those pieces of data will guarantee that there was no MITM (Man-In-The-Middle) attacks on the Diffie-Hellman key exchange. The Diffie-Hellman suffers from a MITM attack.

* How can the PubRK, the endorsement Certificate and the Attestation Signature ensure that there was no MITM attack ?
    - For Diffie-Hellman, the way to defeat the MITM attack is to ask one of the two parties to sign the last message in the exchange and in here, we receive a signature and with this signature, you can verify that it was signed by (thanks to the endorsement certificate) a trusted CPU since we are trusting the CPU manufacturer.

You can also ensure that there are no replay attacks. One replay attack could be to send some code and initial data to have some remote computation in the untrusted infrastructure and the infrastructure does everything in full and then the CPU generates a correct attestation signature and because i am a bad infrastructure manager, I just send that back to the remote client, everything is fine but then the next time the same remote client wnats to run the same remote computation in a trusted way, I could choose the same CPU or different one, it could modify the code or the original data to be loaded in the enclave with a rogue code but then could try to replay the attestation to the remote client to try and fool it to believe that the code sent is the one loaded in the enclave while the code was changed by the infrastructure operator or remote system software.

Why is such an attack defeated by this ? 
Key exchange message 2 is sent by the Secure Container, but to be sent, it needs to be untrusted system software which could actually change that key exchange message 2 and that would be the MITM attack. So this is something different.
Actually, the hash of the key exchange Message 1 contains a nonce which is the message 1 itself which was chosen by the remote client and this is hashed into the attestation. So it is actually the key Exchange message 1 which acts as a nonce and prevents a replay attack.

As it trusts the CPU manufacturer, it can trust the Secure Container with all the mechanisms cited above.

* Enclave Execution
    - User mode and privileged modes on CPU with priviledge memory protection for the priviledged mode
    - New mode which is enclave mode
    - That enclave mode works pretty much like priviledged mode use dto work except that it is controlling access to the PRM and therefore to be able to access PRM (part of the DRAM which is protected), the CPU must be in enclave mode. Because of that, the privileged mode will be banned from accessing the PRM. This is simply how CPU ensures that the untrusted system software cannot go and access the PRM directly otherwise it could modify anything that is in it.
    You have on the CPU an instruction to enter and leave enclave mode as we had intructions to enter and leave privileged mode. One thing the CPU must not do when it is in enclave mode is service interrupt faults or VM_EXIT (what happens when you go from code that runs in a VM into the hypervisor, it is like going from user mode into kernel mode but at the level of the virtual machine). Why ? Because interrupt faults or VM_EXIT, when you are servicing them, you call system software ... interrupt handler, fault handler are in the kernel and the VM_EXIT, you jump straight into the hypervisor but you do not trust those guys so you cannot go and service interrupts faults and VM_EXIT while in enclave mode otherwise you would gie access to the enclave and the PRM to those part of the software and you cannot trust them.
    - So first, when there is an interrupt or fault or VM exit, the CPU must perform what we call an asynchronous enclave exit (AEX).
    - AEX : The CPU saves architecture state (content of the CPU registers for instance) inside the enclave, so the architecture state while in enclave mode is shielded from anything that is not running in enclave mode. Once the states of the registers have been saved, the CPU will load the registers with arbitrary state (to avoid leaking data to the untrusted part of the system because the content of the registers while in enclave mode can then only be accessed when in enclaved mode). In a sense, if you have computation that runs in enclaved mode, that part of the computation has its own context if you want which is saved only inside the enclave. Only when those registers have been "obfuscated" then the CPU will switch modes and jump to the predefined address outside the enclave to service whatever event triggered the asynchronous enclave exit such as an interrupt, a fault or a VM exit.

* How do we get data into the enclave ?
    - We are going to thing about thz confidential data the client want to protect from the untrusted remote system
    - Remote client will most certainly want to get confidential (encrypted) data into the enclave at run-time.
    - We had the Diffie-Hellman protected key exchange between the enclave and the remote client but to get data inside the enclave, we will require input/output such as network access or disk access. All I/O is controlled by the untrusted remote system and that is why you need all of that data to be encrypted.
    - How is the data getting from the I/O subsystem on the remote system into the enclave ?
    - DMA (Direct Memory Access engine on the various devices controllers) cannot be allowed to access PRM. It is because otherwise, as DMA is controlled and configured, set, by the system siftware which you don't trust, the rogue kernel could arrange to rewrite enclave code through DMA after verification of the enclave.
    - Enclave uses the same memory mapping facilities as before. The code running inside the enclave is using the same page tables as we had before we didn't have enclaves. The enclave code can access unprotected memory that is part of the process virtual address space. It is like exactly the same situation as we used to have with the privileged mode. Anything running in privileged mode can access unprivileged memory but anything in unprivileged memory cannot access privileged mode and here it is the same. Anything into the PRM can access memory which is outside the PRM but anything outside the PRM cannot use PRM memory. Don't get it wrong though, the privileged memory where you run the system software is also protected from code running inside the PRM. Anything running into the PRM cannot access privileged memory and vice-versa.
    - Because the enclave code can actually access unprotected memory which is part of its virtual address space (of the associated processes virtual address space), then you can exploit that property to get data inside the enclave. You could for instance stage the I/O operations through buffers in unprotected memory then either have the enclave code copy those buffers into the PRM because the enclave code can access things outside of the enclave but also thing inside the enclave which happens to be in the PRM, or you could have the kernel add the buffers pages to the enclave. We have an enclave mode switch instruction meaning that we must have registered PRM entry points with that instruction. The kernel mounting or adding buffer pages into the enclave, the corresponding unprotected memory pages where you have your buffers could be added into the page tables and marked as being part of the enclave itself, you could do that as long as no enclave entry point registration is modified.
    - The way to do this in the case where the PRM, which is a contiguous block of DRAM, would actually be to have the bottom part for instance of the PRM which is kind of left unprotected at the beginning and as you need more pages, those unprotected pages at the bottom of the PRM would then be turned into PRM pages. This is kind of a faster way to import data into the protected memory. 
    Otherwise, you could simply have the enclave copy code from its unprotected memory into the enclave memory.
    - Problems we had with privileged memory and user' space memory in operating systems are still there. Now, getting data from I/O into the enclave might actually require two copies of the data, you might have a copy of the data from the device into kernel buffers (that are in privileged memory) then the kernel would need to copy the data from the kernel buffers into unprotected user' space memory in the process virtual address space which is what we have today in operating systems and then the trusted code in the enclave would have to copy the data from the untrusted part of the process memory into the enclave. Because the data is going through twice untrusted memory, then only encryption primitives can ensure integrity and confidentiality of that data (hashing, encryption and so on and so forth). Thanks to the protected Diffie-Hellman, we have a symmetric key that has been established between the remote client and the enclave, so we have a way to get data safely into the enclave.

#### Trusted Computing Attacks

* Attack on Enclaves
    - Beware of side-channel attacks (an attack exploiting a speculative execution and then doing a cache timing attack)
    - CPUs are still going to be speculating here. An attacker, remember that the system software could be one of your opponents/adversaries and try to exploit the speculation engine on the CPU to access enclave memory and then through a game of cache timing, recover bits of data out of the enclave memory just as the attacks in side-channels recovered bits of data out of privileged memory.
    - Those attacks are real and present on side-channel attacks but because trusted computing requires modifications on the CPUs, then what the CPU really need to do is either ensure cache partitioning. You could have native cache partitioning mechanisms where you say ok that part of the cache is only to be used when we have enclave mode and the other part when we are not. Or what you can do and of course cache partitioning might have to do this, is to flush the caches on enclave entry and exit. If whenever you do an enclave entry and exit, you flush all the caches then you should be able to protect the cache content. Here, because you want to provide trusted computing, on misspeculation, either you systematically aswell flush the caches or at least flush the partition of the cache that has to do with enclave mode or you could have the CPU even when it is speculating remember that it is gone into enclave mode and then on misspeculation just also flush the partition of the cache that is reserved for enclave mode.
    - Another thing the CPU can do is that when pages are assigned to the PRM, it cancompute which cache lines are used for the corresponding address space and then when an untrusted page uses the same cache lines, it is to always flush those cache lines when there is misspeculation and enclave entry or exit.
    - As you can see, the only way you can defend against those side-channel attacks based on cache timing is to actually throw away performance and do proper cache flushing and cache partitioning.

* EPC Attack
    - Specific attack that a rogue kernel could play on the EPC.
    - The page tables are managed still by the system software so by potentially rogue software and so you might have a situation where part of the page table is correct and you have in the DRAM (part of the PRM) some code for instance that will do some verification before disclosing some secret to the remote client.
    - Correct way this should work : On virtual page 41000, you would have the code for the error (when the verification, the check, fails) and on the page 42000, you would have the code to disclode the secret. What a rogue kernel could do is actually swap those two pages out of the PRM and then swap them back in but by permuting their entry in the page table. Now page 41000 would be mapped onto frame 1A000 and page 42000 mapped onto 19000. So, the two frames are swapped when the pages are brought back in. The kernel can then update the page table correctly? But what happens if you still have previous mapping entries into the TLB, then the MMU using this page table which is correct would get the previous mappings. It would actually get that virtual page 41000 which is suppose to contain the error code mapps onto the physical frame that contains the disclose code and vice-versa. The OS, which can be rogue, could use this attack to try and get the enclave to disclose code when it should not. In modern systems are multicore, so you have multiple TLBs in the system and so by a gam of scheduling the enclaves on different cores at various times, the OS could have tried to populated the various TLBs with the original mappings and then reuse some of those old mappings after the page tables have been updated after the pages have been swapped in the frames.
    - One way to defend from that is that the CPU must actually shutdown all the TLB entries for evicted, for pages that get evicted from the PRM.
    - Before, when a page was being evicted from DRAM, you were not changing the TLB entries but the operating system would only evict TLB entries when the pages would be brought back in to main memory and that the frames in which those pages were brought back in were different from what they used to be. It used to be the operating system that instructed to flush TLB entries but to ensure secure enclaves, now the CPU must shootdown the TLB entries itself whenever a page gets evicted from the PRM and it must do that for all the TLBs on the system.
    - ON EPC page swapping, CPU must shootdown TLB entries for evicted pages as it is the only defence against active memory mapping attack.
    - Without enclaves, it is the operating system that knows when it is evicting a page from RAM onto disk and bringing the page back. It is the oerating system that knows whether a page that has been evicted and is being brought back into main memory is brought back into the same or a different memory frame. The TLB is essentially a cache for the mappings between virtual addresses to physical addresses. So the TLB holds part of recently used pages. So, when you have only user' space and privileged mode, it is actually the operating system when it brings back a page into a different frame from where it used to be, that when the operating system changes the page table, it instructs the CPU to invalidate the corresponding mappings that it might have cached for the correpsonding virtual address.
    But now, the kernel is untrusted, so this guy could be rogue and what he might do is actually mount the attack we have just seen with two pages and swap them back in but swap the frames in which those pages are reloaded. It will update the page tables but it could not tell the CPU that actually the mappings have changed because the attack is to actually swap the content of the two pages to get the enclave to do some thing that it shouldn't do, it shouldn't have disclose and vice-versa. 
    To defend against that, the only thing you can do is not trust the potentially rogue system software to do the right thing and tell the CPU to invalidate the corresponding TLB entries. You cannot rely on the system software to do the right thing. So the defence is that whenever a page is evicted from the PRM and remember, the CPU knows that because the CPU must encrypt that page, so you have  special instruction on the CPU that the system software uses to tell the CPU eject this page. When this happens, the CPU automatically shootdowns (meaning invalidates) all the TLB entries in all the TLBs on the system corresponding to the virtual address in the corresponding asid? of the page being evicted. The CPU does it systematically and does not rely anymore on the system software to do it because you don't trust the system software.

    ![Local Image](/images/trusted/T10.PNG)

* Attacking on Enclaves
    - The only thing you trust in the remote system is the CPU, anything else can be a potential adversery. So the attack surface on enclaves is actually huge.
    - The attacker can have physical access to the hardware, so hardware component instrumentation should be easier for the attacker and that really opens up trusted computing to a wide range of attacks which usually shouldn't have to be considered when you are considering a remote attacker.
    - That leaves trusted computing under an awful number of attacks.
    - The question is : Has the manufacturer really thought about all those potential attacks ? 
    - We saw that an attack from user space on one of the major protection mechanism that they implemented in one of the course.
    - Given that it is much easier for an attacker to attack the trusted computing base, because it has physical access, then for an attacker to acess the mode protection, you can somehow doubt that the CPU manufacturer has really thought about closing all the potential attack vectors. Security is always the same, it's a game of cat and mouse. Maybe they closed everything known at time t, but maybe some attacker will find an attack at time t+1 that the manufacturer didn't think about. To close a door like this, maybe a firmware update might be enough, but changing the whole hardware or architecture might be necessary.
    - Also, can you really trust the manufacturer ? At the end of the day, a year of two ago, there was a big shocking news that came out that actually showed that there is a maximum privileged Minix OS with a web server inside your intel CPU. Why is it there ? INtel said we need an OS inside our own CPU because the CPUs are too complex and to manage them, we need an OS, to do it in software. That I can buy. But why is there a web server in that OS ?
    You have essentially maximum privileged meaning that thing can read any memory enclave, privileged, whatever, ... You have a very privileged OS inside the CPU and that guy has a web server which means that it can communicate with the outside. Intel had some trouble explaining that.
    - To what extent can we trust teh Manufacturer ?

### Side-Channel Attacks

#### CPU and Speculative Execution

##### CPU, Speculative Execution, and Virtual Memory

Actually, the Meltdown attack is an attack on the speculative execution engine.

* CPU basics
    - A long, long time ago, CPUs were following a very simple fetch, decode, execute cycle for instructions

        ![Local Image](/images/channels/C1.PNG)
    
    - Of course, that was not that efficient and you can get much more efficiency by doing pipelining where while you fetch, you are decoding previous instruction and executing the instruction before that. We saw in computation structures the classic pipeline architecture.

        ![Local Image](/images/channels/C2.PNG)

* The Trouble With Memory
    - The trouble with modern computers is memory because modern CPU will probably have several cores that are running somehow around 3 GHz but RAM access latency is still about a 100 nanoseconds. So, if you do the maths by looking at the period of a clock cycle of a CPU and you compare that to the RAL lantency, you quickly realise that RAM access takes about 300 compute cycles from the CPU perspective. So, going to memory is very expensive. You would have to stall the CPU for several hundreds cycles, which isn't good for performance obviously.

* Caches
    - L1 hit $\sim$ 4 cycles
    - L2 hit $\sim$ 10 cycles
    - L3 hit $\sim$ 40 cycles
    - L3 hit (remote core, remote CPU, if you have a multiple CPU system) $\sim$ 100 cycles
    - Miss (meaning you go to memory) $\sim$ 300 cycles
    - Going to memory, even with the cache system interpose can be quite expensive in terms of CPU cycles.

* Achieving Speed
    - To try and achieve speed, one of the things that you need to do is keeping the pipeline full as much as possible but it is not easy at all because RAM throughput is ok, you can get a lot of data out of the RAM fairly quickly but it's a latency that is not ok with RAM access.
    - To try and hide this, what the RAM does is that it actually outputs cache line. Whenever you do a RAM read access and even for write, currency is you want is 64 bytes. So, even if you just want to go and fetch 1 byte, you just got 64 bytes out of it which is the size of a cache line so that you try amortize the overhead and latency of RAM accress across multiple bytes and accesses.
    - So, even L1/L2 cache hit is slow because four cycles is basically down to quarter of your performance. What the CPU will try to do is fetch the instructions and data that it needs in advance. It requires longer pipelines and longer pipelines are more difficult to keep full.
    - One thing that CPU does is that its ALU (Arithmetic logic unit) operates on registers and thanks to that, it is kind of easy to some extend to add parallelism specially in instruction level parallelism.

* Intel ILP µarchitecture (macroarchitecture) (in Intel CPU)
    - It represents the Instructions level parallelism
    - You have those executions units at the microcode level (micro operations level) and there is a lot of parallelism there. Intel replicates functional units there so that they can have different functional units executing in parallel for different instructions. They call them executions units here but in computation structures, that was called functional units. There were these reservation stations wihch were just buffers implementing queues to basically access those units.
    - We are going to talk with high level instructions but what we will talk about actually applies to the micro operations.

    ![Local Image](/images/channels/C3.PNG)

* The Case for ILP
    - What is Instruction Level Parallelism ?
    - We have this kind of very simple piece of code where we have 6 instructions that don't that much but illustrate the point. If values are in registers and we can do one operation per CPU cycle, then this code will take 6 cycles.

    ![Local Image](/images/channels/C4.PNG)

    - We could go "superscalar" if we have several execution units and use only 3 cycles if values are in registers and two opertions can be done per cycle.
    - A superscalar processor is an advanced type of CPU architecture that aims to exploit instruction-level parallelism by executing multiple instructions simultaneously within a single clock cycle. It achieves this through multiple execution units, dynamic scheduling, and techniques to handle instruction dependencies. While it offers significant performance advantages, the complexity and diminishing returns present challenges in its design and implementation.

    ![Local Image](/images/channels/C5.PNG)

    - This works of course if the first pipeline has no dependency between variables or values of first operations and the other operations' variables and value.

    ![Local Image](/images/channels/C6.PNG)

    - But if you look in the second line, one instruction compute v and the second one uses the result of the computation of v but you can't use values while you are computing it.

    ![Local Image](/images/channels/C7.PNG)

    - What you can do is differ the execution to run in parallel with another non interfering execution

    ![Local Image](/images/channels/C8.PNG)

    - But then you have two iddle pipeline slots and it is not that great as the pipeline isn't full but still, you reduce from 6 to 4 cycles.
    - But there are no dependies between certains executions

    ![Local Image](/images/channels/C9.PNG)

    - You could move some instructions to empty slots of previous stages and so on.
    - You can execute the code in 3 cycles. You have to execute the instructions in a out-of-order way.
    - Every modern, CPU or a lot of them, uses those techniques and execute code out-of-order. But all the instructions must be shown in order so that as a user and a programmer, you actually don't see that those instructions are executed out-of-order. What you get is that the code that otherwise would have taken 6 cycles has taken 3 cycles to be executed. You have a big performance gain.

    ![Local Image](/images/channels/C10.PNG)

* Out-Of-Order (OOO) executions
    - Instructions are executed out-of-order
    - Instructions are retired in order still
    - The way it is implemented is that you have a reorder buffer and instructions are tagged with their place in the reorder buffer when there are dispatched then after being dispatch they get executed out-of-order and then instructions are retired from the head of the buffer and so the buffer forces the retirement of the instructions to be in order. 
    - But you don't always know which is going to be the next instructions because in programs, you have conditionals. To know which branch of a conditional you are going to take, you need to resolve a condition, to resolve the condition, you might have to access the memory to get to variables that are part of your condition. So that would stall the pipeline but to try and keep the pipeline full, what speculating CPUs do is that they use branch rediction.

* Branch Prediction
    - Speculating CPUs try to make a guess to know whether a branch is taken a not and once they have taken the guess, they just keep speculating following their guess. If the guess is right, then it is great because they will have gone ahead and executed the right piece of code but if the guess is wrong then what needs to be done is to flush the pipeline because we have been doing useless work and then resume the execution in the correct branch which is the other branch then the one where we decided to go.

* Speculative Execution
    - Without speculation on the branch, 7 cycles needed to execute the piece of code

![Local Image](/images/channels/C11.PNG)

    - With Speculation and if we take a good guess

![Local Image](/images/channels/C12.PNG)

    - Our guess, the code inside the branch will be executed. You can execute that code at the same time as the code that is before the branch because there are actually no dependencies between different instructions.
    - Once you know whether v is equal to 0, you can commit the result of those speculative executions.
    - The way it works is that while it is speculating, you can be using temporary registers and when you commit the instructions because you speculated right, you essentially copy those temporary registers into the normal registers. Actually, you mark the temporary registers that have the speculated results as acting as the normal registers.
    - If you take a bad guess, you speculatively execute the instructions but then when you finally resolve the value of the condition, if it is false, in this case you speculated wrong, you went into the branch but we aren't going into the branch and what you do is just discard the results of the speculation, flush the pipeline to remove all traces of the bad speculation and go and fetch the next instruction.

![Local Image](/images/channels/C13.PNG)

#### Virtual Address Space

![Local Image](/images/channels/C14.PNG)

* Process Virtual Address Space
    - Processes run in an virtual address space and that virtual address space is made of two parts : the user space and the kernel space.
    - All your code is working with virtual addresses which basically represent an address space where the process essentially thinks that it owns the whole of memory and they all start at 0 or whatever and every process just plays in its own address space as though it was on its own without having to worry about what addresses other processes use because they all use their own virtual address space.
    - Now, this virtual address space of a process needs to be mapped onto physical memory and the mapping is done through the page table which impelments essentially a function to transform a virtual address of a process into a corresponding physical memory address.
    - This is obviously through the operating system that manages the page table of a process and it is the operating system that has to worry about not mapping the pages from various processes onto the same physical memory addresses.

    ![Local Image](/images/channels/C15.PNG)
    - Something very important to remember is that we have the CPU in two mode of execution, the user mode and the privileged mode.
    - There is part of the memory which can only be accessed when we are in privileged mode and that is of course where we put the kernel so that user programs cannot modify the kernel nor access the kernel data.
    - Kernel space is actually mapped into the virtual address space of each process to basically speed up interrupts and system calls so that we don't need to switch when the user space uses a system call or when an interrupt occurs.
    - If a CPU which is in user mode tries to access kernel space, then we should have a trap and actually what corresponds to kernel space or privileged memory can be decided by the operating system when it is mananging the page tables simply by flicking a bit. There is a bit corresponding to each page table that tells the CPU whether the corresponding memory is privileged or not.
    - Why does mapping kernel into process virtual address space speeds up interrupts/system calls ? It is due to the reduction in the need to switch between different memory address spaces.
    Modern operating systems operate in two modes: user mode and kernel mode. User mode is where user applications run, while kernel mode is where the core OS functions and hardware interactions occur. When a system call or interrupt occurs, the CPU must switch from the user mode (user address space) to the kernel mode (kernel address space). In systems where the kernel is mapped into a separate address space from user processes, switching from user mode to kernel mode involves changing the entire address space context. This switch typically involves changing the page tables and performing a TLB (Translation Lookaside Buffer) flush to ensure the new address space is correctly mapped. TLB flushes can be costly because the TLB is a cache that stores recent translations from virtual addresses to physical addresses. The process of switching address spaces and flushing the TLB introduces significant overhead. This overhead can be particularly impactful when system calls or interrupts are frequent, as the CPU spends a considerable amount of time just performing these context switches.
    By mapping the kernel into the virtual address space of each user process, the kernel and user space share a single address space.This configuration means that switching from user mode to kernel mode does not require changing the address space or flushing the TLB. Reduced Overhead: The key advantage is the elimination of the overhead associated with switching address spaces. When a system call or interrupt occurs, the CPU only needs to switch modes (user to kernel), not the entire address space. Faster Access: Since the kernel code and data are already mapped into the process’s address space, the CPU can quickly access kernel functions and data without the need for additional memory management operations. Keeping the TLB entries intact by not switching address spaces means the CPU can continue to use cached address translations, leading to faster memory access times. This efficiency is particularly beneficial for system calls and interrupts, which often require quick access to kernel code and data.
    - While mapping the kernel into the process address space improves performance, it also introduces security concerns:
        * Isolation: Care must be taken to ensure that user processes cannot access or modify kernel memory. Typically, this is managed through page table permissions that allow user processes to execute system calls but prevent them from directly accessing kernel memory.
        * Kernel Page Table Isolation (KPTI): Modern processors and operating systems have introduced techniques like KPTI to mitigate security vulnerabilities (e.g., Meltdown) that can arise from having the kernel mapped into the process address space.

    ![Local Image](/images/channels/C16.PNG)
    - On modern 64-bit computers, actually, the whole of the pysical memory is mapped into the kernel as the kernel needs to access the whole of the memory so the whole of the physical memory finds a mapping into the virtual address space of every process. This is going to be quite interesting when we start looking at the attacks.
    - That mapping is in kernel space and therefore is privileged memory and when the running process is in user mode it should not have access to that mapping and therefore process, despite the fact that the whole of physical memory is mapped into its own virtual address space, should not be able to go and read or write physical memory that it is not supposed to be accessing. 

#### Meltdown

* First Side-Channel Attack 

![Local Image](/images/channels/C17.PNG)

* Meldown Attack
    - We have some code with a branch.
    - The code of the attack is inside the branch.
    - The process which is supposed to run in user mode will try to go and read kernel memory 

    ![Local Image](/images/channels/C18.PNG)
    - Reading kernel memory when a process is in user mode is an illegal access and should trap.

    ![Local Image](/images/channels/C19.PNG)
    - The problem of course is that inside the branch, we are going to read kernel memory while the CPU is speculating. So the idea is that while the CPU is speculating, if a trap occurs, that trap should be delayed until the moment the speculation engine has figured out that it was speculating right and the trap should only occur when the corresponding instruction would have been executed in normal program execution order. Remember that those CPUs are also doing out-of-order execution so you can't just go and trap a the very moment the speculation engine finds an illegal instruction because you are speculating so you might be doing things that the program wouldn't do anyway and you are executing out-of-order so to keep things clean and give proper signals back to the programmer or the user, you need to delay the trap until the moment the corresponding execution would have occur. This is the essence of the attack. It is to try and do things you are not supposed to do and make the most out of it before things trap.
    - The attack is really after the speculation engine and so if the CPU thinks that the branch will be taken, what it can do is start executing the code of the branch before the branch as explained earlier.
    - The code computing w_, x_, y_, z_ is executing in parallel with the other code.
    - If the branch is taken, we will have to commit the temporary results of the speculation.

    ![Local Image](/images/channels/C20.PNG)
    - First instruction is obviously illegal because the process is in user mode but it can't fault at that moment because the CPU is speculating on the code.

    ![Local Image](/images/channels/C21.PNG)
    - If the branch is taken, it is essentially once we know that the branch is indeed taken that the fault should occur.
    - The essence of the attack is to do something you shouldn't do while the CPU is speculating and you have time until the branch prediction is resolved to be sure it is speculated right for the fault to occur.

    ![Local Image](/images/channels/C22.PNG)
    - If the branch is taken and we fault here at the entrance of the branch, obviously all the results will be discarded as though those instructions inside the branch never ran and the values would be discarded and therefore not be exposed to the process running in user mode.

    ![Local Image](/images/channels/C23.PNG)
    - Until January 2018, we thought that thanks to the flushing of the badly speculated instructions, the kernel memory was not revealed and therefore the whole thing must be saved.

    ![Local Image](/images/channels/C24.PNG)
    - Why does it work ? Because the access to kernel memory runs completely unchecked and the legality of this memory access done during the speculation is checked in parallel to the memory access because the result of the check only needs to be ready when we enter the branch. When we enter the branch, meaning when we would have entered the branch at the moment when the condition is resolved and known, so after speculations.

    ![Local Image](/images/channels/C25.PNG)

* Meltdown Attack : How Does It Work ?
    - Attack on the speculation engine which runs the code

    ![Local Image](/images/channels/C25.PNG)
    - The speculation goes ahead and reads kernel memory without checking whether the code doing it runs in user mode or privileged mode.

    ![Local Image](/images/channels/C26.PNG)
    - Get the value that read and mask one bit of it.
    - It extracts the least significant bit of the value that was read (the rightmost bit) and so "x" will be 0 or 1.

    ![Local Image](/images/channels/C27.PNG)
    - Then compute "y" which is either 0 or 4096
    - Why 4096 ? Because caches never do precaching across page boundary. You are basically making sure that in the last instruction, you are gonna go and read values which are in an array but those values live on different pages.
    - A common page size is 4096 bytes (4 KB).
    - CPU caches are organized into cache lines, which are typically 64 bytes in size. When data is fetched from memory, an entire cache line is loaded into the cache.
    - By using a stride of 4096 bytes, the attacker ensures that each access is on a different memory page. Since typical page sizes are 4096 bytes, each access with an offset of 4096 bytes accesses a new page.
    - Accesses within the same page (within 4096 bytes) could potentially be cached in the same cache line. By accessing data with a stride of 4096 bytes, each access is in a different page and therefore likely to be in a different cache line.
    - Caches do not prefetch across page boundaries. This means if an access causes a cache miss, the cache will fetch only the specific cache line containing the accessed data, and not cross into the next page.
    - Here’s how the use of 4096 ensures effectiveness in the Meltdown attack:
        * Access Pattern: The attacker arranges for speculative execution to access a sequence of memory locations in an array, each separated by 4096 bytes.
        * Cache Timing: After speculative execution, the attacker measures the access time to these array elements. Due to the side-channel effect, the access time reveals which cache line was loaded into the cache.
        * Page Isolation: By ensuring that each access is on a different page, the attacker avoids potential prefetching and ensures that the observed cache effects are due to the speculative execution crossing page boundaries.

    ![Local Image](/images/channels/C28.PNG)
    - That value of y is used as an index in an user mode array.
    - In the last instructions, you read one of two specific locations (0 or 4096) in user space which is completely legal because you can always read user space data irrespective of the mode in which the CPU is. User mode can read user space data but privileged mode can also read user space data.

    ![Local Image](/images/channels/C29.PNG)

* Meltdown Attack : How Does It Work ? (Continuous)
    - When unrolling the bad speculation (which is the case here), user space code should not have gone in the branch, the CPU will discard the temporary registers and also the queued memory writes. While you are speculating, if you the code wants to write data back into memory, you don't go and update the values in memory because you are speculating so you might be doing the wrong thing so you have a write buffer where you queue memory writes and only actuate modifications of memory when the corresponding instructions are actually retired which means that the speculation was right.
    - Anything you have speculated while you were badly speculating and executing code you were not suppose to execute will not be reflected into main memory because all the queues with memory writes and all the temporary registers will be discarded when you figure out that the speculation was wrong. 
    - The one thing that does not happen is that the cache content stays unchanged. That is the other vector that allows the attack to work.
    - We could have think that while we are speculating, we are accessing memory for reading values and those values obviously get cached into our caches. You could think that when the CPU realizes that it speculated wrong, it would be a good idea from a safety perspective to flush cache but from a performance perspective all the cache would be cold. Trying to improve performance through speculation would then resort when you speculated wrong in big loss of performance if you flush the cache, you are also flushing out all the cache content that was acquired legally when executing previous instructions. So the cache content stays unchanged.
    - This is the side effect of the attack. The side effect of executing the last instructions `z_=user_mem[y_]` persists in the cache. Whichever value you read in the user_mem array was cached and is still in the cache.
    - What the attacker needs to do is making sure that either user_mem[0] or user_mem[4096] is in the cache and to do that, one must evict the corresponding cache line before the code that is executed. It will try to evict the value from the cache before the attack.
    - To do this, you have instructions, for instance `clflush` (unprivileged) that allows you to flush a cache line or you could try and get the cache line evicted if you do not have a CPU that have the flush instruction by loading appropriate values from appropriate addresses from main memory that are competing with cache lines that you are trying to evict but to do this, you can do a loop in your program that keeps loading memory addresses that you know are on the same cache line then the values you are trying to evict but to this, you need to know the structure of the cache (bit more complicated and most of Intel CPUs have the cacheline flush instruction).
    - All the attacker needs to do is arrange for either v to be different from zero for our branch condition would be false and the CPU would realize that it misspeculated and it would revert back its speculation and the fault would not occur.
    Or you can arrange to handle the fault (tell the operating system that if such a fault occurs, call this fault handler and you can be the owner of the fault handler).
    Or new features and new CPUs called transactional memory where you can do/undo a whole block of instructions and essentially instruct the CPU to behave as though nothing happened. Nothing happens in our case means cached values persisting in the cache ...
    - All that is now needed for the user space code is to time access to `user_mem[0]`.
    - Can do that by using the `rdtsc` (tick counter) available on the CPU or any other timing technique.
    - Start a clock before accessing `user_mem[0]` which is user space data and you are in user mode so it is legal access, and once you have the answer, you stop the clock and if the accessing this value is fast (few ticks), then you know that the bit you isolated `x_` in the attack code (least significant bit of some word in privileged memory) was a 0 because you derived the index that you are using into the array from that bit. Remember, You read value in the array as the last instruction of the attack. If accessing this value is slow, it means the value was not in the cache, and remember you evicted this value from the cache before the attack, then it means that what the attack code did, when the CPU speculated, was to read a 1, because what ends up in the cache in that case would be `user_mem[4096]`, that would be the fast one to read. Reading value 0 being slow, you know that what you read was 1 from the kernel.
    - In other words : after speculative execution, the attacker times access to user_mem[0] and user_mem[4096].
        * If `x_` was 0, `user_mem[0]` is accessed (fast if cached).
        * If `x_` was 1, `user_mem[4096]` is accessed (fast if cached).
        * If access to `user_mem[0]` is slow (many CPU ticks), it indicates `x_` was 1, as `user_mem[0]` was evicted from the cache during the attack and `user_mem[4096]` was cached
    - By multiplying by 4096, you ensure that the resultant memory access falls into a different page, thus ensuring that cache behavior changes based on the bit value.
    - In other words, `user_mem[0]` leaks a bit from the kernel and the way it works is that it is escalating a µarchitecture side-effect (which was leaving some value inside the cache due to speculation even undone speculation) into an architecture side-effect.
    - In this case, the cache is a covert channel. Some code has done something that has left the cache in a certain state and some other piece of code is then using the cache to guess a value that was read illegally during speculation by the other piece of code.
    - The attack is essentially a race against the trap/fault
        * if `z_ = user_mem[y_]` gets executed, the bad guy wins because through the cache side channel, it can recover one bit of kernel memory through a timing attack.
        * in fact, the branch statement is not really needed in our case, could mount that attack without the branch prediction simply by letting the speculation engine go ahead. The code is very short, so it is fearly easy for the attacker to have that code run by speculation and have the code finished running before reaching the moment the trap should happen. If you put it in a branch, you can arrange for that branch to never be taken and so you don't have to deal with the trap as it won't happen.
    - Now we have seen how to steal one bit from the kernel. Then if we can do this, we can steal anything from the kernel. All you need to do is start again with the next kernel bit that is of interest to you. For the next kernel bit, you can change just the value of the mask to extract another bit when `x_ = w_&0x01`.
    - Remember that the whole of the physical memory is actually mounted into the kernel and in the process virtual address space, so anything in physical memory can be stolen. Which is great because not only you can steal values inside the kernel but also inside the memory of other processes. Needless to say, passwords are no longer protected by memory protection of CPUs.
    - This attack is very robust (low noise).
    - `y_=x_*4096` is to make sure both locations are on different pages, as cache prefetching never occurs across page boundaries (that lowers the noise in the attack). It could just happen if the values are too close to eachother, cache prefetching could prefetch both values and that introduce noice for the attacker because then the timing attack might give wrong results.
    - The guys who have implemented this attack did some measurements and they showed that leakage rate from the attack can reach up to $\sim$ 500kB/s. Only takes a few seconds to scam the whole memory. Very powerful attack.

* What happen if the trap occurs when the access to `user_mem` during the attack has not finished yet ? On that round, the attack fails. No leak. The attacker can restart the attack on that particular bit of course. To win the bit, the attacker must win the race with the trap therefore that corresponding value must reach the cache before the trap.

* How does the attacker know the attack fails ?
    - If the value you read takes a long time to come back, you could either say then it is the other value that worked. You could be wrong. Maybe the read was long because the trap occurs before value read is cached.
    - If the read is long, you decide to read the other value and if it is also long, you know the trap won that race. The second read only slows down the attack. It doesn't stop it.

* Meltdown Attack : Countermeasure
    - Everything told during the operating systems course is now a big lie because hardware protection model with the two modes (privileged and user mode) is broken. It completely bypasses those protections.
    - In our case the operating system cannot be modified, it is a read attack but that everything you write inside the operating system and also inside main memory even other processes can be read. Nothing can be changed but the attacker has full read access to the whole of main memory.
    - If hardware is broken, software -> OS

* Meltdown Countermeasure : KPTI
    - KPTI : Kernel Page Table Isolation
    - The problem is that the kernel space which contains the whole of the physical memory inside it is available inside the virtual address space of the process so now we are going to cut this virtual address space into two page tables. We are going to have a page table for user space and a separate page table for kernel space. The idea is that you can't access addresses that are not mapped into your address space. When the process is running, it will be the part of the user space virtual address space which is accessible. While the CPU will be trying to speculate, the MMU won't be able to get the corresponding physical addresses corresponding to kernel space addresses because that mapping table will not be available to the MMU. Therefore, if the MMU is stuck, the CPU won't be able to speculate.

    ![Local Image](/images/channels/C30.PNG)
    - More realisticly, we are going to have some interrupt/syscalls entry points still mounted in user space part of the process virtual address space and it is in these calls that the page table and the address space IDs (ASIDs) will be switched so that the MMU loads the corresponding kernel space when we have an interrupt or system call. During speculation this mechanism will let the CPU keep speculating on system calls and nothing else, the switch will also be automated. That's a fairly simple defense, you just split in a sense the virtual address space of the process and only expose either the user space or the kernel space so that speculation cannot, when in user mode, access kernel space unless it is through system calls. System calls don't let you go and read anything you like in the kernel.

    ![Local Image](/images/channels/C31.PNG)

* Meltdown Countermeasure : Impact
    - Entry/exit info/from interrupt/syscalls become very expensive because changing the page table means that almost pay a complete context switch. You do that on system calls and interrupt and that is the reason why the kernel space used to be mapped to the whole of the virtual address space of the process.
    - That penalty has been measured, by the game of the TLB/ASIDs, keeping some of the entries warm in the TLB, depending on the I/O load, the performance penalty can be between 40% and 60%. You have programs that slow down up to 60%, which is quite significant.

* Meltdown : What's Impacted ? 
    - All Intel CPUs (since $\sim$ 1995)
    - ARM : Cortex A15, A57 and A72
    - AMD claims they run check before mem access and stall the speculative execution (claim = not really proven)
    - Containers (container = kernel on steroids, still have a single kernel for the different containers and this kernel was mapped into the virtual address spaces of the processes)
    - Paravirtualization (hypervisor is also mapped into the virtual address space of the processes because with paravirtualization, what the process needs to do is that the process needs to transform some of its syscalls to its guest, "local", kernel straight onto a paravirtualized call to a corresponding system call in a sense in the Hypervisor so Hypervisor's space was mapped also in the virtual address spaces)
    - Full virtualization : no cross VM leak because the Hypervisor completely isolates the VMs.

#### Specter 1

![Local Image](/images/channels/C32.PNG)

* Spectre 1 : Bounds Check Bypass
    - Let say we have access to two arrays in main memory and arrays are in user space.
    - A check on the bound of the array.

    ![Local Image](/images/channels/C33.PNG)
    - The attack access an index in one of the arrays
    - The idea is to actually bypass the check for instance, x could be further than the end of the array and then you extract one bit from the value you just read, you do the trick of computing an index which is either 0 or 4096 and then you go and read in a second array at that index a value and by timing another access to this value in the second array, you will be doing the same trick as trying to guess what bit you have stolen as Meltdown.

    ![Local Image](/images/channels/C34.PNG)
    - That is the main strategy as in Meltdown attack.

    ![Local Image](/images/channels/C35.PNG)
    - Javascrypt engine does this, JIT (Just-In-Time Compiler), try and make sure that indices are in bound.
    - For the attack to work, the attacker must make sure that the `array1_size` value is not in cache. We saw with the Meltdown attack that you have unprivileged instructions to flush cache lines out of the cache or you can do it by repeatedly loading values that you know share the same cache line as `array1_size` but to do the latest you need to know the structure of the cache, much easier to do if you have a flush instruction. 

    ![Local Image](/images/channels/C36.PNG)
    - The attacker might need to train the branch predictor to take a branch. It might need to perform a few in-bounds accesses to `array1` beforehand so that the branch predictor start thinking ok this branch is almost always taken so i'll speculate by taking.

    ![Local Image](/images/channels/C37.PNG)
    - The attack is any x the idea being since `array1_size` is not in the cache, it is going to take some time for the speculation engine to retrieve the value from memory and therefore it would speculate blindly on any x and it is only when `array1_size` would be resolved that it will see that it should not have speculated by executing this code.
    - The idea is that any x means you can go and read any values outside `array1` because bound check is not done at the moment you go and speculate.

    ![Local Image](/images/channels/C38.PNG)
    - If again, `array2[0]` and `array2[4096]` are evicted from the cache, before the attack, we know exactly what is going on because we found something similar in the Meltdown attack. By just timing access to one of those two values after the attack we can then guess whether the value that was read basically corresponds to bit 0 or 1 of the bit that we are stealing from the value.

    ![Local Image](/images/channels/C39.PNG)
    - When `array1_size` finally gets resolved, the CPU unrolls the mis-speculated instructions and the cache is not flushed for mainly performance reasons and so the attacker just needs to time `array2[0]` in the normal following code that follows the speculation

* Spectre 1 is not Meltdown
    - `array1` is legally accessible by attacker. Remember when in Meltdown, what the attacker was doing was reading some kernel memory which does not have the right to read when in user mode. `array1` is actually here a user mode array which is part of the process address space. The attack is against the bounds check, not the memory protection system.
    - Spectre 1 is an attack against bounds check and Meltdown is a race against memory access check.
    - Spectre 1 is a race against RAM access (because the attacker has to make sure that `array1_size` is not in the cache so that the system needs to go and retrieve the value from RAM). And, RAM latency is much slower so it is easier to win the race.
    - In Meltdown, the memory access check is much faster because what the MMU needs to do is just to check the bit, the corresponding protection bit of the page.

* Why use Spectre 1 ?
    - It is essentially yo break sandboxing. If you have code that is trying to sandboxe other code than it will be using boundchecks a lot to make sure that the code stays in its playground and by using spectre 1 attack, you can try and escape the sandbox.
    - Example :
        - When you have a Javascrypt code that runs in a browser tab, actually the browser tab is represented by a thread and that thread runs within the context of the brwoser's process. And all those threads share processes address space. Of course, what the Javascrypt engine is trying to do is to sandbox each scrypt so that the scrypt running in one browser tab cannot access data from different browser tab. But with this attack, the attacker can get to any data in any tab. If you visit a website with a rogue scrypt in it and you just happen to have for instance your bank on another then the attacker could actually get some fairly interesting data from the banking site.
    
* Spectre 1 : Countermeasure
    - For OS, there is actually nothing wrong because the code that we are running is accessing user space data.
    - Because of that, there is no easy defence
        * some "serialization instructions" on some CPUs that seem to halt speculative execution but there is no guarantee that this happens because it seems to depend on the specific implementation of those instructions in the specific CPU models. Te compiler could insert these instructions but of course, switching off speculation results in a huge performance hit
    - One thing that we can do, the Compiler or the interpreter can do a branchless checks, probably the easiest thing to do. Instead of doing an if and check the value of x against the maximum size of the array, is simply mask the index with an array bound mask and obviously this can only work well if the size of the array is a power of two.
        * `array1[x & array1_bound_mask]`
    - We might be forced with this to create arrays that are bigger than what we really need resulting in a little bit of internal fragmentation in a sense.
    - This defense is simple, can be used everywhere at the expense of a small price. You can let the speculation still run and have the benefits of speculation.

* Spectre 1 Countermeasure in Browsers
    - Make timing more difficult for instance by reducing the precision of timing sources. That is one thing you can do easily, say that our browsers can no longer have direct access to the tic counter for example.
    - Another thing that was available in Javascrypt was SharedArrayBuffers where you could tell the Javascrypt engine to actually share buffers across different scrypt and by disabling this you would prevent one scrypt to provide timing for another. Of course a lot of web applications used that by disabling SharedArrayBuffers, a lot of web applications broke but this was the emergency solution chosen by browser vendors. The browser vendors decided that it was preferable to break some web applications than to leave this very important and dangerous security gap in their browser.

* Spectre 1 : What's Impacted ?
    - All Intel and AMD CPUs were impacted
    - Most ARM CPUs

#### Specter 2

*  Spectre 2 : Branch Target Injection
    - Spectre does branch target injection.
    - The idea is that in a lot of branches, you have an indirect target for the branch meaning that the jump destination is loaded from memory.
    - You are jumping through a pointer. The jump target is in a variable and you need to retrieve that variable to retrieve the jump target. That's called an indirect branch instruction.
    - Branch prediction is we take the branch yes or no. But now you can speculate on pretty much anything and so to be able to speculate in the case of an indirect branch instruction, you actually don't know where you need to jump. The speculation engine can actually try and guess where the code is gonna jump and we are going to see what it is using. It is using some kind of history of where the corresponding branch has jumped in the past to go ahead and jump to a specific target when it actually has no idea whether the target is still valid or not.

* Branch Target Buffer (BTB)
    - That history is actually, so the jump target history is actually called the branch target buffer. It stores the last few destinations (target) addresses for each jump instructions (source address).
    - Values that we find in that BTB is used to speculate on jump targets so that speculation engine can run ahead and it might for instance do some kind of majority vote on where to go.

    ![Local Image](/images/channels/C40.PNG)

* BTB bits are expensive
    - The only problem is that those BTB are quite expensive because it is a table. It is bits, the information you put in there, it is taking space on the CPU. It is consuming CPU real estate. What the CPU manufacturers do is that they try and keep the functionality or pretty much the target prediction as good as if supported by a full size branch target buffer, but by reducing the number of bits that they store in that table. For instance what they do when we say the source address of the jump, they actually represent the source address by some upper bits of the source address. They are kind of discarding some of the lower bits of the address and what it does is that now you have a many to one mapping. You can have several distinct source addresses that all share the same upperbits that are kept and therefore, they will be maped onto the same entry of the branch target buffer. Therefore, their target will be shared in the data.
    - BTB also assumes that some number of the target upper bits are the same as the source meaning you never jump too far in your code so you assume that you jump close by from where you jump, you can then not store the full target address and discard upper bits as they will be the same as source address. This could introduce a little bit of noise because your real target could be outside of the range that is permitted by the lower bits that you keep for the target but then that would just be bad speculation and so be it.
    - Not only we have a many to one mapping from different sources address to the same entry of the BTB, but then also we can have some noice that is introduced in the target computations themselves because values being recorded might actually be lacking some bits.
    - This means BTB is some form of hash table with some kind of noisy values inside it. That is exactly what the attacker can try and exploit.
    - BTB is a complex piece of kit and because it is a complex piece of kit, it is often shared between the hyperthreads of a core. You have a single branch target buffer per core even if that core has several hyperthreads. You can already smell what the attacker can do, if the attacker manages to run on different hyperthreads of the same core as the core that it is trying to attack, it is then very easy for the attacker to somehow "pollute" the values that the BTB holds. The attacker can quite easily choose the values for the targets that are inserted in the BTB and stear essentially where the speculation should go and speculate when it is speculating for the victim code

* Spectre 2 : Attack Principle
    - The attacker just needs to find a "gadget" that it wants to run victim. A "gadget" is a code already present in the victim (part of the normal code of the victim) and if that code observable side effects, then the attacker can through the side channel access those observable side effects because it would have streared the speculation engine to run the corresponding gadget in the victim while the speculation engine was speculating for the victim.
    - Just need to find a source address of an indirect jump taken often by the victim.
    - Then, pollute the BTB entry correesponding to that indirect jump and stear it to the gadget that you ve selected and to do this, the attacker can use a timing attack on the BTB. Because the BTB is the same for the attacker and the victm. The attacker can run a bunch of indirect jump inside its own code and by timing it, it can figure out whether the speculation engine is speculating a lot or not on its own code and by looking at the source of the indirect jumps in the attacker's code then the attacker can figure out what are the likely sources that are being used by the victim.
    - Once the attacker has found the source that is of interest, then it needs to start doing a lot of indirect jumps from an address that maps to the same source bits in the BTB and of course those indirect jumps are in the attacker's code and simply jump to an address of interest to the attacker but in the virtual address space of the victim.
    - The attacker then pollutes or misstrain the BTB with its chosen target so that the next time the victim jumps indirectly from a corresponding source, then, the speculation engine will follow the target that was chosen by the attacker.
    - Remember that the source and target addresses do not need to be completely exact, so it is easier to find proper sources and proper targets that will give you the results that the attacker wants.
    - When the speculation engine speculates for the victim, the target is inside the victim's address space but before mounting the attack, the attacker will have maybe through opensource or whatever or by instrumenting the code of the victim or running the code of the victim with profiling or whatever, will have chosen appropriate gadgets, appropriate targets that leave exploitable side effects for the attacker.
    - That was the hard part, now all the attacker needs to do is to eevict the real jump target from cache and then go and observe the side-channel.

* Spectre 2 : Good News and Bad News
    - Good news : harder to deploy than other two attacks. The attacker needs to do a lot of analysis on the victim's code to select gadgets etc.
    - Bad news : potentially much more powerful than the other attacks. You can't inject code but you can choose what existing code gets mis-speculated.

* When would I want to use Spectre 2 ?

* Spectre 2 : Impact on System Call Interface Mechanism ? 

![Local Image](/images/channels/C41.PNG)

This is the system call interface mechanism that the OS uses to let user applications call in services from the kernel. Guess what ? We are going through a table and this table implements indirect branching. So, whenever you call a system call, you have an indirect branch. 

The whole system is supposed to be able to constrain where the users space code can get the kernel space to jump and only at specific entry points for the system calls but now, as we have just seen, through pollution of the branch target buffer, an attacker could actually change those entry points and get the kernel to jump anywhere inside the kernel. That is a pretty bad situation.

![Local Image](/images/channels/C42.PNG)

* Spectre 2 : Impact on Code ?

![Local Image](/images/channels/C43.PNG)

Take this C++ code as example. In the C++ inheritance mechanism, you have dynamic binding. You can have two classes, one `Base` class, which has a `Foo()` method and another `Derived` class from the `Base` class that also has a version of the `Foo()` method. If somewhere you say ok I have a pointer to a `Base` object and you put a pointer to a `Derived` object into that. If you call `Foo()` on the object, because using it through a pointer, then you will have dynamic binding. The runtime will do dynamic binding and would actually compute that it is the `Foo()` method that it needs to use because the `Foo()` method in the `Base` was declared as virtual.

To support this kind of mechanism, of dynamic binding, the dynamic binding is resolved at runtime using vtable (indirect branch).

The attack is not only on the system call interface but also all over C++. That is a fairly dramatic potential that this attack has.

* Spectre 2 : Countermeasures
    - Serialization of instructions can help but always bad for performance
    - Firmware updates where the CPU manufactuers release new firmware for processors and on the new processors, they implemented indirect branch restricted speculation (IBRS), an implementation to stop the CPU from speculating on indirect branches. With that, performance penalties is quite small (only loose about $\sim$ 10% of the performance).
    - On older CPUs, no hardware fix, need to do something else.
    - That something else was done by security researchers at Google and was called the Retpoline.
    - Retpoline = Return Trampoline
    - That is a very clever defense against those kind of attacks. This is a compiler defense.
    - The idea is to get the compiler to replace the indirect branches with code that will force the processor into useless but safe speculation.
    - The compiler in a sense will be the one to switch off speculation but because the compiler has no way to tell the CPU stops speculating because the CPU is built to speculate, the compiler will thus generate code that will force the CPU to speculate on useless loops.

* Spectre 2 : Retpoline for Jump *%r11
The way it works is this : if you have a jump to an indirect target, that is the jump %r11 implementations, before the attack, what the compiler would have done was to simply issue this instruction as such and what this instruction does is that in the register 11, you actually have the address where the target address is in memory. So that you indirect through the value inside r11 to go and fetch, so, inside the register, you have the address in main memory where the address of the target is.
Instead of just issuing this assembly instruction or corresponding machine instruction which the compiler use to do, what it will do is replace that instruction with the little code as shown.
![Local Image](/images/channels/C44.PNG)

It will do a direct call to `set_up`. The target for `set_up` is actually in the instruction, so no speculation here. And when you do a call to a function and here this is a function call in a sense, the return address from the call which in this example should be the address of the `capture`, should be put on the stack. What the compiler does here in the `set_up`, what the `set_up` does, it says the return address, I don't want the one that is done by the call instruction, I want you to move into the stack at the place where there is a return address, I want you to move the value that you find by indirecting through the register 11. This move instruction here will place the target address in the stack at the place where the return address from the `set_up` function is.
So, `set_up`, when it returns, should return eventually to the branch target address.
What you want is that your code jumps to a branch target address. And that branch target address is in main memory and the address of main memory where it is is in register 11. When you do the call instructions, part of the instruction will save on the stack using the stack pointer which is `rsp` to save the return address where you need to return after the function, in this case, the address in memory corresponding to the `capture` label because we call a function, we go to return, we carry on executing. So, what `calls set_up` instruction will do is that it will load address of `capture` where the return address from `set_up` function should return.
I am going to move into the place where we have saved the return address from myself and move the branch target address, so when returning, we should go at the branch target address which will result in the equivalent of jumping to the branch target address.
That branch target address is sitting in RAM and it is going to take time for the CPU to get to it.

This moving completes a lot of CPU cycles because values we are after needs to come from main memory.

Then the function `set_up` finishes and we are going to return, but we have no idea where.

![Local Image](/images/channels/C45.PNG)

Even if we knew where we are going, the cache line representing the return address that has been saved in the stack could go missing from the cache because it could be evicted.

![Local Image](/images/channels/C46.PNG)

You have a buffer on the speculation engine of the CPU that basically stores the return addresses that come from call instruction.

When you do a call instruction, that instruction puts on the stack that return address but also puts a copy of that return address in the RSB.

So here, we are going to have a copy of the address of the `capture` label on the RSB and it also goes onto the stack.

But at the same time, when we finish the `set_up` function, the speculation engine will use the RSB to know where to return.

![Local Image](/images/channels/C47.PNG)

The speculation engine will just do this until it knows it speculated right or wrong. It will know that when we finally get the branch target address out of memory. The speculation will that oh wait a minute, the value we had to jump to was actually not the address it thought. It will undo speculation and jump at the right place which is the place given by the value that was retrieved from the address contained in the register 11 in this case which is branch target for the indirect jump.

![Local Image](/images/channels/C48.PNG)

As long as the CPU doesn't know where you wanted to jump exactly, it will speculate and here we force it by using a direct call as opposed to an indirect jump, we force it to speculate by doing nothing. That is why it is called a returned trampoline because as long as the speculation engine doesn't know where it needs to return because where it needs to return comes from RAM, it will just jumps endlessly like it is jumping on a trampoline.

![Local Image](/images/channels/C49.PNG)

![Local Image](/images/channels/C50.PNG)

![Local Image](/images/channels/C51.PNG)

![Local Image](/images/channels/C52.PNG)

![Local Image](/images/channels/C53.PNG)

Google also disabled the use of hyperthreading in the cores (another solution) because those BTB were shared between hyperthreads.

Retpoline is a software construct that prevents speculative execution of indirect branches by ensuring that the CPU doesn't speculate on the target of indirect jumps. It works by redirecting indirect jumps to a controlled sequence of instructions that safely handle the return address without allowing speculation to occur.

Direct Call (call set_up):

The call set_up instruction is a direct call to the set_up function. Since it's a direct call, pushing the return address onto the stack, there is no speculation involved at this point.
Capture Label:

After the set_up function returns, the CPU continues execution at the capture label.
The capture loop (pause; jmp capture;) is an infinite loop with the pause instruction. The pause instruction is a hint to the CPU that it is in a spin-wait loop, which can help optimize power usage and resource allocation while waiting.
The jmp capture; instruction is an unconditional jump back to the capture label, creating a loop.
Set_up Function:

Inside the set_up function, the instruction mov %r11, (%rsp); stores the value in the r11 register into the stack pointer location.
The ret; instruction pops the return address from the stack and jumps to it. However, because of the modifications done earlier, this return address is controlled and does not lead to speculative execution.
Preventing Speculation:

Indirect Call Speculation:

Normally, an indirect call or return could cause the CPU to speculate the target address, which could lead to executing unintended instructions. Spectre attacks exploit this by manipulating the speculative execution path.
Return Stack Buffer (RSB):

The RSB is a CPU feature used to predict the return address for functions. It can be manipulated by attackers to exploit speculative execution.
By using retpoline, we ensure that the return address placed in the RSB is controlled and does not allow speculation to unintended targets.
Capture Loop:

The pause and jmp capture; loop keeps the CPU busy in a controlled manner until it is safe to execute the return instruction without speculative execution.

In other words :
The CPU pushes the return address (which would be the instruction following call set_up) onto the stack and jumps to set_up.
The mov %r11, (%rsp); instruction writes the value in r11 to the memory location pointed to by the stack pointer (%rsp), overwriting the original return address with the value in r11.
The ret instruction then pops this address from the stack and jumps to it.
Assuming r11 was set to the address of the capture label, the CPU jumps to capture.
In the capture loop, the pause instruction hints to the CPU that this is a spin-wait loop.
The jmp capture; instruction creates an infinite loop, ensuring the CPU does not speculatively execute beyond this point.
By modifying the return address to point to a controlled location (capture), the retpoline sequence ensures that the CPU does not speculatively execute an indirect branch. This is the essence of the retpoline mitigation against Spectre variant 2:
The CPU is forced to execute the capture loop without speculating on the next address.
This controlled loop prevents the CPU from executing unintended instructions speculatively, thereby mitigating the risk of leaking sensitive data through speculative execution side channels.

* Spectre 2 : What's Impacted ?
    - As far as we know, all speculating processors.

* Conclusions
    - Fundamental isolation assumptions from hardware on which the OS rely heavily are broken.
    - The speculation is breaking all of this, the world is not what we all thought it was.
    - Need a complete CPU architecture redesign
    - Guys went to Intel and agreed to wait before showing the world this attack to have time to patch things.
    - But, new version of CPU means $\sim$ 300 engineers working for $\sim$ 5 years and that is just for a "delta" improvement (new features implemented only)
    - How long for a full redesign ?
    - Big redesign challenge
    - Need to fix this shit without loosing too much performance which is really hard to do.
    - No CPU vendor inclined to throw away years of performance squeezing experience that easily.
    - In the meantime, users will continue to pay good money for high-perf CPUs, deploy software that basically throw away the performance in order to (somehow) regain some security
    - Expect more bugs of this type !
    - And since then (since the teacher did the slides) they did !
    - Side channel attacks is essentially using some mechanisms to indirectly leak data. Meltdown and Spectre 1 is a timing attack on caching. Specter 2 is essentially exploiting buffers in the speculation engine to control where the speculation engine goes and then recover through some side channels some data that your are not supposed to access.

### Fuzzing

#### What is Fuzzing ?

* Fuzzing
    - Fuzzing or Fuzz Testing
    - It is basically the process of finding security vulnerabilities in input-parsing code by repeatedly testing the parser with (fuzzed) inputs.
    - You have a piece of software that is accepting inputs from users and you are trying with fuzzing to make sure that the part of the program that is dealing with that input essentially does it well regardless of the shape of that input.
    - It has been a mainstream practice in assessing software security for two decades now and also a mainstream for attack strategy. There are some hackers that fuzz test bunch of applications to try and find ways to exploit possible vulnerabilities left in the input parsing code.
    - What are the inputs we are talking about here : documents, images, sounds, videos, network packets, network requests , web pages, etc., anything that you are submitting for input to a program.
    - Can submit inputs to local software or remote software (speaking to a server on a network for instance)

* Why Fuzz ? 
    - Many applications deal with untrusted inputs encoded in complex data format (like in web development, json, netflix and its encoded videos)
    - Corresponding code is large, complex, using low-level constructs for performance. If you want your parsers to be really fast (on most applications but especially in the cloud, you have a tendency to use low-level programming languages so parsing is especially fast). The lower-level you are, the less safe guard the language gives you such as bound checks on buffer usage etc. The more opportunities there is for programmers to make mistake and leave what would be buffer overflow bugs in their software. If you have a bufferoverflow then there is a possibility for memory corruption and depending on the context, some of those can be exploited by an attacker to inject their own piece of code and have the local software execute the code controlled by the attacker, of course not a good situation to be in from a security perspective.

* Buffer Overflow Consequences
    - Elevation-of-privilege attack
        * Possible hijacking the execution to run its own malicious code.
    - Information disclosure attack
        * Steal internal information (trick the application into releasing information that should not have been released but simply by confusing the application about where the boundaries of the buffers are, the application could send back information it shouldn't to the attacker).
    - Denial-of-Service attack
        * Crash application. This is not so much a security risk but depending on the settings, if you can mount a DoS attack on systems that control the utility networks of a country. If you can bring down control servers for electricity grid, DoS can have fairly serious consequences.

* Security Vulnerabilities vs Exploits
    - Vulnerabilities : programming errors (bugs) triggered under specific conditions (e.g. buffer overflow). You trigger the vulnerability by sending inputs data that is inconsistent through the program. It can be triggered so for some inputs the vulnerability is deactivated and no memory corruption for some inputs and only under specific inputs conditions you can suffer memory corruption.
    - Exploit : piece of data/code (as you can put code in the data) that triggers vulnerability and takes advantage of it for malicious purposes. Those purposes can be any of the attacks we talked about, DoS, ...
    - Not every vulnerability is exploitable but when it is exploitable, could lead to complete control of the host system by the attacker. It is always better to try and avoid as many vulnerabilities as possible.

#### Detecting Security Vulnerabilities In Software

1. Static Program Analyser
    - Tool that inspects the code and reports unexpected/known bad code patterns
    - Easier to be performed on source code but there are some static analysers that work on binary code.
    - It is really a developper's tool but some of it can be done by anyone as anyone can get the binaries of the software.
    - The problem is that it gots a high rate of false positive. It could flag some code as bad simply because it doesn't recognize those patterns but it is not always the case that piece of code are flag and are problematic resulting in a vulnerability.
    - Higher the false positive rate the less useful the tool is.
    - Trade-off between completeness and performance. The more code pattern you put in the static analyser the longer it takes to analyse a piece of code.
    - Static analysers catch easy bugs, but misses a lot of bugs. Specially useful as programmers make the same mistake all the time but it doesn't guarantee that there isn't any other bugs.
2. Manual Code Inspection/Testing
    - Peer-reviewing of code and/or design/run predetermined inputs.
    - Penetration testing is manual code inspection/testing specifically for security purposes. Either security specialits looking at the code if they have access to the code or attacking the code with malicious inputs to try and uncover vulnerabilities that might still be in the code.
    - Problem is that it is labour-intensive and expensive and does not very scale, if very large piece of software, the corresponding code can be very large and testing a good chunk of it would require a lot of people.
    - Can catch serious bugs.
3. Fuzzing
    - Repeatedly execute application with all kinds of input variants
    - How do you produce that input so that you are confident that you are exercising all of the input parsing code and therefore get high confidence that you have tested thoroughly the input parser and hopefully detected bugs it might have ?
    - Requires test automation (picking the inputs to be fed is the most difficult part). Designing strategies that will come up with the right inputs to pick for the tests is very difficult
    - Ideally requires rest of the application state after each iteration because you want to actually not only feed all sorts of variants to the applications but also to analyse what is going on once you ve done it so you must reset the application. One input might have corrupted one part of memory of the application but maybe the pplication hasn't crashed nd you haven't seen any sign of that corruption, if you don't reset application state then, further down the line, after you have tried more tests, you could have a crash that resulted from previous inputs. This is not always possible for an attacker and much more difficult in distributed seetings (cloud, multi-tier applications, etc.)
    - No false positive (false negative if you haven't reset the state as explained but if you have a crash you are certain to have a bug)
    - Computationally intensive (sfor alone developper, it is inconvenient or use cloud services to fuzz test softwares)
    - Provides inputs to reproduce and analyse the bug as you know which one you fed that caused the bug. You might have some fuzzed inputs causing an application to crash but during the analysis of the bug, you would be looking when you understood where the bug is, you would be trying to reverse engineer some inputs that might not only retrigger the vulnerability but maybe also exploited. An input that uncover vulnerability might not be completely telling the story on what the inputs should look like so that the vulnerability can be exploited for other purpose than crashing. So, other inputs can exploit uncovered vulnerability.
    - Can still miss bugs but has found thousands of bugs in last decade

#### Main Fuzzing Strategies

##### Blackbox Fuzzing

* Blackbox random fuzzing
    - Tests application with random mutations of well-formed inputs
    - Software considered under test as a blackbox. No assumptions as to how it is build. Do not try and exploit knowledge about how it is built.
    - Blackbox testing can always be done on a system where you have no access to the code being sourced or the binary code.
    - Blackbox is based on generating random inputs.
    - Application ran with runtime checking tool (e.g. valgrind, etc) in conjunction with feeding random inputs to try and catch non crashing bugs (memory leaks, signs of memory corruption only runtime checking show, etc.).

* Example of a Blackbow Random Fuzzer

![Local Image](/images/fuzzing/F1.PNG)

You give it a `seed` input which is a well formed input for the program and then this will randomly choose how many mutations it needs to do on the well formed input that it was given and here it takes a fixed rate of mutations $\sim$ 1000 bytes and then it will compute a new input based on the well-formed input it was given and takes between 1 and up to 1/1000th of the byte and replace those bytes at random with a random value. New mutated input computed and executes the application with the new computed input and see what happens.

Effectiveness depends on diverse set of well-formed seed inputs. We need a set of inputs that when fed to the application can execice as much of the input parsing code as possible. We need inputs that will cover the various options and encoding supported by the application for the various formats and the idea if you have a set of well-formed seed inputs that cover a lot of the possible cases of different options and format variations, then, fuzzing, random flipping of bytes or bits (byte level better because a lot of formats encode information at the byte level), then, those mutations are likely to exercice more execution path throughout the whole parser.

Blackbox fuzzing can be done with purely random inputs (as originally done). But the problem is that the application will generally detect that input is completely garbage and will very quickly discard that input. Repeatedly feeding pure random inputs to the application results in poor code coverage because repeatedly the same part of the parser being exercised. Purely random input unlikely to produce input incrementally good and force the parser to detect or not the erros further down the parsing tree.

By doing more targeted randomization, then, we limit the noise and we test more error handling code in different parts of the application which is always good. Although it is better than completely random inputs, the probability of generating new interesting inputs with random mutations is still fairly low.

Blackbox fuzzing is easy to do, useful but it still has limited bug uncovering power.

##### Grammar-based Fuzzing

What is needed with grammar-based fuzzing is the specifications of the application input format as an input grammar. In that grammar, when you specify that grammar to a grammar-based fuzzer, the tester can also tell what input parts are to be fuzzed and how. Much better control to what kind of inputs the fuzzer will be generating -> target precisely parts of inputs needs to be fuzzed so that we can hopefully uncover bugs.
Once we have that kind of grammar, the fuzzer can generate many inputs and runs them against the application.
Very general approach and some grammar-based fuzzers also include programmatic constructs methods and recursion that can be encoded inside the grammar to have fairly complex input generating construct. The fuzzer can be directed into generating very complex fuzzed inputs.

* Example

This is like a language to code the grammar and the `s_string` command simply defines a constant string. When the fuzzer sees a line like this, it will simply output that `POST / api/blog/ HTTP/1.2 ` string.

![Local Image](/images/fuzzing/F2.PNG)

It tells the fuzzer to output the size of `blockA` as a 2 character string. 

![Local Image](/images/fuzzing/F3.PNG)

Then, we have the code that declares or defines `blockA`. We have the start of the block instruction and the end of the block instruction.

![Local Image](/images/fuzzing/F4.PNG)

And then we have inside the block two constant strings that will just be outputed. And the `s_string` variable is code that instructs the fuzzer to output a first string. Some of the grammar-based fuzzers have dictionaries of fuzzed strings that they would go and get, replace and output each of the inputs in their dictionary at various parts of the code. Can have one dictionary for each `s_string` variable declared.
It is in the way that you populate the various dictionaries that you control exactly how the inputs are fuzzed.
Using a dictionary reduces this noise by focusing on inputs that are more likely to be significant.

![Local Image](/images/fuzzing/F5.PNG)

![Local Image](/images/fuzzing/F6.PNG)

Grammar-based Fuzzing is very powerful but it requires user expertise to focus input towards corner cases, inputs that are more likely than others to create problems.

It is great for structure data, json, xml, network protocol. The more structured the data is, the more likely just random mutations might put the inputs in a state that is easily detectable as erronous. For instance, if parser is looking for a field called "data" and now it has changed to "date", it would be very easy for the parser to figure out that the data is malformed. 

Writing grammar is laborious.

##### Whitebox Testing

It consists in executing program under test dynamically. The idea is while you are doing this, you gather constraints on inputs from the conditional branches encountered during the execution of some inputs and then once you got the constraints, to negate them one-by-one, and use a constraint solver to resolve and derive new inputs and then those new inputs are then fed to the program and the idea is that if one input has followed an execution path inside the code, whenever you found the conditional instruction, you know whether the condition was taken or not for the input that you had and so this is where you can derive constraints on the inputs. You know you had such and such constraints on the input because such and such branches where true or false and then by negating one-by-one those constraints then the idea is that deriving new inputs from the negation of those constraints, you will have inputs that will explore new branches in the execution path.

The idea here is to very quickly increase the code coverage of the test by being extremely clever in the way inputs are generated. Itis an attempt to sweep through all the execution paths. 

Practicaly, you cannot hope to do complete code coverage but it can already explore many executions paths and cover a big pourcentage of the input parse code.

You do this in combination with a runtime checker. Actually use a runtime checker for any type of fuzzing where you have the piece of software locally because fuzzed inputs could crash the application but sile fuzzed inputs could create memory corruptions that doesn't immediately result in a crash but you could have some other side-effects that the runtime checker could uncover.

* Example

Quick look at whitebox testing example of a function that simply takes an integer as an input and then computes another integer from it and if that computed integer takes a specific value, there is an error in the code represented as an abort here. Else everything is fine represented as returning zero.

![Local Image](/images/fuzzing/F7.PNG)

What a whitebox testing might do is to try and test this with an input value of zero.

![Local Image](/images/fuzzing/F8.PNG)

It will then find that it has gone through the else branch of the if as the if branch has not been taken (semantically equivalent to being an else clause). 
The symbolic execution will find that there is a constraint on the path of the ELSE branch and that the constraint will be that $x + 3 \neq 13$

![Local Image](/images/fuzzing/F9.PNG)

The path constraint will be negated and so the constraint being negated is that $x + 3 = 13$. That negated constraint is passed to a constraint resolver that will comeback and sy x must be equal to 10. Then, the whitebow fuzzer will then use $x = 10$ as the next input and obviously by doing this, we have a new path in the execution path that gets explored and in this case we uncover the error.

![Local Image](/images/fuzzing/F10.PNG)

![Local Image](/images/fuzzing/F11.PNG)

Whitebox testing generates inputs that will be fed to the program in a much more dirven way and the strategy is to explore as many execution paths as possible in a very short time. A little note, if you are trying to test this piece of code on a 64-bit machine using blackbox testing, you would have only one out of $2^{64}$ chances to find this bug because just mutating the input here, it is only one out of $2^{64}$ inputs that will uncover the bug. Whitebox testing is much more efficient and effective here at uncovering bugs than blackbox testing.

![Local Image](/images/fuzzing/F12.PNG)

Whitebox testing can theoretically provide program verification (total coverage) tests that cover the totality of the code, all the execution paths. But in practice, the number of execution paths explode exponentially especially if code is complex. A branch multiplies the number ...
There are also things in modern programming languages that render symbolic execution and contraints generation and solving very imprecise such as pointer operations, floating-point, system calls, libraries in a sense that there is no precise solution in the symbolic execution, constraint generation and solver in reasonable practical time.
Therefore, the success on good whitebox testing also relies on good seed inputs because again good seed inputs can start the whole process on various paths on the input parser and therefore really stear the whitebox fuzzing into good code coverage.

Whitebox testing these days works at machine code level. It is on one hand very good because a lot of students have taken the compiler class and have seen that a lot of transformations are applied to the code when it is transformed from source code to binary format. The binary format can be a lot more complicated than it looks on the source code. You have a lot of metadata on programs such as the variable names, function calls, and so on and so forth that get obfuscated during the binary transformation on the source code. Machine code level is what is being run by the system and being able to whitebox the machine code is very interesting.
On the other hand, the bad news is that whitebox testing is then also available to an attacker who can require the binary of the application.

There are many optimizations created to increase the code coverage of huge applications. That is a whole research field. Because of that, whitebox testing finds many more bugs than other approaches.
There is a guy called Patrice Godfroid who has a PhD from university of Liege who is leading efforts about whitebox testing in Microsoft and thanks to his works, Microsoft has been able to put out software where thousands of bugs have been put out before release. Those softwares are still buggy but less, try and leave as few bugs as possible. Easiest bugs have been uncovered.

##### Conclusions

Fuzzing is routinely used at major software providers. Cloud settings complicate fuzzing because no access to binaries. Blackbox and grammar-based fuzzing always available to an attacker. If you do not fuzz, someone else will do it for you.

Whitebox fuzzing sometimes available to attacker. If binary is available but not for remote fuzzing attacks.

Fuzzing is actually used mostly for security purposes but can also be done for generic software quality strategies.