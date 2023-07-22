const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

async function main(params) {
    const {__ow_method, IAM_API_KEY: apikey, COUCH_URLy} = params
    const authenticator = new IamAuthenticator({apikey})
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(COUCH_URL);
    if (__ow_method === 'post') {
        await cloudant.setServiceUrl(params.COUCH_URL);
        const doc = params.review;
        const id = doc.id || Date.now()
        try {
            cloudant.postDocument({db: "reviews", document: doc})
            return {"dbs": id};
        } catch (error) {
            return {error: error.description};
        }
    } else if (__ow_method === 'get') {
        const id = parseInt(params.dealerId)
        try {
            const {result: {docs}} = await cloudant.postFind({
                db: "reviews", selector: {dealership: id},
            })
            return {"dbs": docs};
        } catch (error) {
            return {error: error.description};
        }
    }
    return {error: 'not found'}
}