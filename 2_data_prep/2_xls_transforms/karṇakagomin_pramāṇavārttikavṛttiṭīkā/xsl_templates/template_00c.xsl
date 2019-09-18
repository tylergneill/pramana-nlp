<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<!-- 
<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="body/p|body/lg">
<p>
<xsl:copy-of select="./@*"/>

<xsl:attribute name="pb_n">
<xsl:value-of select="preceding::pb[@ed='s'][1]/@n"/>
</xsl:attribute>

<xsl:copy-of select="./node()"/>
</p>
</xsl:template>

<xsl:template match="body/quote">
<quote>
<xsl:copy-of select="./@*"/>

<xsl:attribute name="pb_n">
<xsl:value-of select="preceding::pb[@ed='s'][1]/@n"/>
</xsl:attribute>

<xsl:copy-of select="./node()"/>
</quote>
</xsl:template>
 -->


<xsl:template match="/">
<TEI><text><body>
<xsl:apply-templates select="/TEI/text/body/p|/TEI/text/body/lg|/TEI/text/body/quote"/>
</body></text></TEI>
</xsl:template>

<!--specific template match for this img -->
<xsl:template match="/TEI/text/body/p|/TEI/text/body/lg|/TEI/text/body/quote">
<xsl:copy>

<xsl:apply-templates select="@*" />

<xsl:variable name="curr_pb_n">
<xsl:value-of select="./@pb_n"/>
</xsl:variable>

<xsl:attribute name="pb_n2">
<xsl:value-of select="count(preceding-sibling::*[@pb_n=$curr_pb_n])+1"/>
</xsl:attribute>

<xsl:apply-templates select="node()" />
</xsl:copy>
</xsl:template>

<!--Identity template copies content forward -->
<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>


</xsl:stylesheet>

<!-- 
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="p">
<p>
<xsl:copy-of select="./@*"/>

<xsl:variable name="curr_pb_n">
<xsl:value-of select="./@pb_n"/>
</xsl:variable>

<xsl:attribute name="pb_n2">
<xsl:value-of select="count(preceding-sibling::p[@pb_n=$curr_pb_n])+1"/>
</xsl:attribute>

<xsl:copy-of select="./node()"/>
</p>
</xsl:template>

</xsl:stylesheet>
 -->