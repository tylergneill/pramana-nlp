<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="/">
<TEI>
<text>
<body>
	<xsl:for-each select="/TEI/text/body//quote[@type='base-text']">
		<xsl:copy-of select="./node()"/>
	</xsl:for-each>
</body>
</text>
</TEI>
</xsl:template>



</xsl:stylesheet>