const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({apikey: params.IAM_API_KEY})
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);
    const {state:st, dealerId: id} = params
    try {
        const {result:{docs}} = (st || id) ? await cloudant.postFind({db: "dealerships", selector: {st, id}})
            : await cloudant.postAllDocs({db: "dealerships", includeDocs: true})
        return { "dbs": docs };
    } catch (e) {
        return {error: error.description};
    }
}
